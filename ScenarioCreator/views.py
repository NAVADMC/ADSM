from glob import glob
import json
import os
import shutil
from django.core.management import call_command
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.db import connections
from django.conf import settings
import re
from ScenarioCreator.models import * # This is absolutely necessary for dynamic form loading
from ScenarioCreator.forms import *  # This is absolutely necessary for dynamic form loading
from Settings.models import SmSession
from django.forms.models import modelformset_factory
from django.db.models import Q
from django.forms.models import inlineformset_factory


# Useful descriptions of some of the model relations that affect how they are displayed in the views
singletons = ['Scenario', 'Population', 'Disease', 'ControlMasterPlan', 'OutputSettings']
abstract_models = {
    'Function':
        [('RelationalFunction', RelationalFunction),
         ('ProbabilityFunction', ProbabilityFunction)],
    'DiseaseSpread':
        [('DirectSpread', DirectSpread),
         ('IndirectSpread', IndirectSpread),
         ('AirborneSpread', AirborneSpread)]}

def spaces_for_camel_case(text):
    return re.sub(r'([a-z])([A-Z])', r'\1 \2', text)


def unsaved_changes(new_value=None):
    session = SmSession.objects.get_or_create(id=1)[0]  # This keeps track of the state for all views and is used by basic_context
    if new_value is not None:  # you can still set it to False
        session.unsaved_changes = new_value
        session.save()
    return session.unsaved_changes


def scenario_filename(new_value=None):
    session = SmSession.objects.get_or_create(id=1)[0]  # This keeps track of the state for all views and is used by basic_context
    if new_value:
        session.scenario_filename = new_value.replace('.sqlite3', '')
        session.save()
    return session.scenario_filename


def activeSession():
    full_path = settings.DATABASES['scenario_db']['NAME']
    return os.path.basename(full_path)


def home(request):
    return redirect('/setup/Scenario/1/')


def extra_forms_needed():
    missing = list(ProductionType.objects.all())
    for entry in ProductionTypePairTransmission.objects.all():
        if entry.destination_production_type_id == entry.source_production_type_id:  #Spread within a species
            missing.remove(entry.source_production_type)
    extra_count = len(missing)
    if not missing and ProductionTypePairTransmission.objects.count() < ProductionType.objects.count() ** 2:
        #all possible interactions are not accounted for
        extra_count = 1  # add one more blank possibility
    return extra_count, missing


def production_type_permutations():
    spread_assignments = []
    pts = list(ProductionType.objects.all())
    for source in pts:
        for destination in pts:
            spread_assignments.append(ProductionTypePairTransmission.objects.get_or_create(
                source_production_type=source, destination_production_type=destination)[0])  # first index is object
    return spread_assignments


def disease_spread(request):
    assignment_set = production_type_permutations()
    SpreadSet = modelformset_factory(ProductionTypePairTransmission, extra=0, form=ProductionTypePairTransmissionForm)
    try:
        initialized_formset = SpreadSet(request.POST, request.FILES, queryset=ProductionTypePairTransmission.objects.all())
        if initialized_formset.is_valid():
            instances = initialized_formset.save()
            print(instances)
            unsaved_changes(True)
            return redirect(request.path)  # update these numbers after database save because they've changed

    except ValidationError:
        initialized_formset = SpreadSet(queryset=ProductionTypePairTransmission.objects.all())
    context = {'formset': initialized_formset}
    context['title'] = 'How does Disease spread from one Production Type to another?'
    return render(request, 'ScenarioCreator/AssignSpread.html', context)


def save_formset_succeeded(MyFormSet, TargetModel, context, request):
    try:
        initialized_formset = MyFormSet(request.POST, request.FILES, queryset=TargetModel.objects.all())
        if initialized_formset.is_valid():
            instances = initialized_formset.save()
            print(instances)
            unsaved_changes(True)
            context['formset'] = initialized_formset
            return True
        return False
    except ValidationError:
        return False


def populate_forms_matching_ProductionType(MyFormSet, TargetModel, context, missing, request):
    """FormSet is pre-populated with existing assignments and it detects and fills in missing
    assignments with a blank form with production type filled in."""
    if save_formset_succeeded(MyFormSet, TargetModel, context, request):
        return redirect(request.path)
    else:
        forms = MyFormSet(queryset=TargetModel.objects.all())
        for index, pt in enumerate(missing):
            index += TargetModel.objects.count()
            forms[index].fields['production_type'].initial = pt.id
        context['formset'] = forms
        return render(request, 'ScenarioCreator/FormSet.html', context)


def assign_protocols(request):
    missing = ProductionType.objects.filter(protocolassignment__isnull=True)
    ProtocolSet = modelformset_factory(ProtocolAssignment, extra=len(missing), form=ProtocolAssignmentForm)
    context = {'title': 'Assign a Control Protocol to each Production Type'}
    return populate_forms_matching_ProductionType(ProtocolSet, ProtocolAssignment, context, missing, request)


def assign_progressions(request):
    """FormSet is pre-populated with existing assignments and it detects and fills in missing
    assignments with a blank form with production type filled in."""
    missing = ProductionType.objects.filter(diseaseprogressionassignment__isnull=True)
    ProgressionSet = modelformset_factory(DiseaseProgressionAssignment,
                                          extra=len(missing),
                                          form=DiseaseProgressionAssignmentForm)
    context = {'title': 'Set what Progression each Production Type has with the Disease'}
    return populate_forms_matching_ProductionType(ProgressionSet, DiseaseProgressionAssignment, context, missing, request)


def initialize_relational_form(context, primary_key, request):
    if not primary_key:
        model = RelationalFunction()
        main_form = RelationalFunctionForm(request.POST or None)
    else:
        model = RelationalFunction.objects.get(id=primary_key)
        main_form = RelationalFunctionForm(request.POST or None, instance=model)
        context['model_link'] = '/setup/RelationalFunction/' + primary_key + '/'
    context['form'] = main_form
    context['model'] = model
    return context


def deepcopy_points(request, primary_key, created_instance):
    queryset = RelationalPoint.objects.filter(relational_function_id=primary_key)
    for point in queryset:  # iterating over points already in DB
        point = RelationalPoint(relational_function=created_instance, x=point.x, y=point.y) # copy with new parent
        point.save()  # This assumes that things in the database are already valid, so doesn't call is_valid()
    queryset = RelationalPoint.objects.filter(relational_function_id=created_instance.id)
    formset = PointFormSet(queryset=queryset) # this queryset does not include anything the user typed in, during the copy operation
    return formset


def relational_function(request, primary_key=None, doCopy=False):
    """This handles the edge case of saving, copying, and creating Relational Functions.  RFs are different from any
    other model in ADSM in that they have a list of RelationalPoints.  These points are listed alongside the normal form.
    Rendering this page means render a form, then a formset of points.  Saving is more complex because the points also
    foreignkey back to the RelationalFunction which must be created before it can be referenced.

    It is possible to integrate this code back into the standard new / edit / copy views by checking for
    context['formset'].  The extra logic for formsets could be kicked in only when one or more formsets are present."""
    context = initialize_relational_form({}, primary_key, request)
    context['formset'] = PointFormSet(instance=context['model'])
    if context['form'].is_valid():
        unsaved_changes(True)  # Changes have been made to the database that haven't been saved out to a file
        if doCopy:
            context['form'].instance.pk = None  # This will cause a new instance to be created
            created_instance = context['form'].save()
            context['formset'] = deepcopy_points(request, primary_key, created_instance)
            return redirect('/setup/RelationalFunction/%i/' % created_instance.id)
        else:
            created_instance = context['form'].save()
            context['formset'] = PointFormSet(request.POST or None, instance=created_instance)
        if context['formset'].is_valid():
            context['formset'].save()
            if request.is_ajax():
                return ajax_success(created_instance, "RelationalFunction")
            return redirect('/setup/RelationalFunction/%i/' % created_instance.id)
    context['title'] = "Create a Relational Function"
    return render(request, 'ScenarioCreator/RelationalFunction.html', context)


def ajax_success(model_instance, model_name):
    msg = {'pk': model_instance.pk,
           'title': spaces_for_camel_case(str(model_instance)),
           'model': model_name,
           'status': 'success'}
    return HttpResponse(json.dumps(msg), content_type="application/json")


def save_new_instance(initialized_form, request):
    model_instance = initialized_form.save()  # write to database
    unsaved_changes(True)  # Changes have been made to the database that haven't been saved out to a file
    model_name = model_instance.__class__.__name__
    if request.is_ajax():
        return ajax_success(model_instance, model_name)
    return redirect('/setup/%s/' % model_name)  # redirect to edit URL


def new_form(request, initialized_form, context):
    if initialized_form.is_valid():
        return save_new_instance(initialized_form, request)
    return render(request, 'ScenarioCreator/crispy-model-form.html', context)  # render in validation error messages


def get_model_name_and_form(request):
    model_name = re.split('\W+', request.path)[2]  # Second word in the URL
    form = globals()[model_name + 'Form']  # IMPORTANT: depends on naming convention
    return model_name, form


def get_model_name_and_model(request):
    """A slight variation on get_mode_name_and_form useful for cases where you don't want a form"""
    model_name = re.split('\W+', request.path)[2]  # Second word in the URL
    model = globals()[model_name]  # IMPORTANT: depends on naming convention
    return model_name, model


def initialize_from_existing_model(primary_key, request):
    """Raises an ObjectDoesNotExist exception when the primary_key is invalid"""
    model_name, form_class = get_model_name_and_form(request)
    model = form_class.Meta.model.objects.get(id=primary_key)  # may raise an exception
    initialized_form = form_class(request.POST or None, instance=model)
    return initialized_form, model_name


'''New / Edit / Copy / Delete / List that are called from model generated URLs'''
def new_entry(request):
    model_name, form = get_model_name_and_form(request)
    if model_name == 'RelationalFunction':
        return relational_function(request)
    initialized_form = form(request.POST or None)
    context = {'form': initialized_form, 'title': "Create a new " + spaces_for_camel_case(model_name)}
    if model_name not in singletons:
        context['model_link'] = '/setup/' + model_name + '/'
        context['pretty_name'] = spaces_for_camel_case(promote_to_abstract_parent(model_name))

    return new_form(request, initialized_form, context)


def edit_entry(request, primary_key):
    model_name, form = get_model_name_and_form(request)
    if model_name == 'RelationalFunction':
        return relational_function(request, primary_key)

    try:
        initialized_form, model_name = initialize_from_existing_model(primary_key, request)
    except ObjectDoesNotExist:
        return redirect('/setup/%s/new/' % model_name)
    if initialized_form.is_valid() and request.method == 'POST':
        initialized_form.save()  # write instance updates to database
        unsaved_changes(True)  # Changes have been made to the database that haven't been saved out to a file

    context = {'form': initialized_form,
               'title': str(initialized_form.instance),
               'pretty_name': spaces_for_camel_case(promote_to_abstract_parent(model_name))}
    if model_name not in singletons:
        context['model_link'] = '/setup/' + model_name + '/' + primary_key + '/'
    else:  # for singletons, don't list the specific name, just the type
        context['title'] = 'Edit the ' + spaces_for_camel_case(model_name)
    return render(request, 'ScenarioCreator/crispy-model-form.html', context)


def copy_entry(request, primary_key):
    model_name, form = get_model_name_and_form(request)
    if model_name == 'RelationalFunction':
        return relational_function(request, primary_key, doCopy=True)
    try:
        initialized_form, model_name = initialize_from_existing_model(primary_key, request)
    except ObjectDoesNotExist:
        return redirect('/setup/%s/new/' % model_name)
    if initialized_form.is_valid() and request.method == 'POST':
        initialized_form.instance.pk = None  # This will cause a new instance to be created
        return save_new_instance(initialized_form, request)
    context = {'form': initialized_form,
               'title': "Copy a " + spaces_for_camel_case(model_name)}
    return render(request, 'ScenarioCreator/crispy-model-form.html', context)


def delete_entry(request, primary_key):
    model_name, model = get_model_name_and_model(request)
    model.objects.filter(pk=primary_key).delete()
    unsaved_changes(True)
    return redirect('/setup/%s/' % model_name)


def list_per_model(model_name, model):
    context = {'entries': model.objects.all()[:200],
               'class': model_name,
               'name': spaces_for_camel_case(model_name)}
    return context


def promote_to_abstract_parent(model_name):
    for key, value in abstract_models.items():  # fix for child models (DirectSpread, RelationalFunction) returning to the wrong place
        if model_name in [x[0] for x in value]:
            model_name = key
    return model_name


def model_list(request):
    model_name, model = get_model_name_and_model(request)
    model_name = promote_to_abstract_parent(model_name)
    context = {'title': "Create " + spaces_for_camel_case(model_name) + "s",
               'models': []}
    if model_name in abstract_models.keys():
        for local_name, local_model in abstract_models[model_name]:
            context['models'].append(list_per_model(local_name, local_model))
    else:
        context['models'].append(list_per_model(model_name, model))
    return render(request, 'ScenarioCreator/ModelList.html', context)


'''Utility Views for UI'''
# Leave this code here until we can use it for importing chunks of a scenario in the Scenario Builder
# def create_db_connection(db_name, db_path):
#     needs_sync = not os.path.isfile(db_path)
#
#     connections.databases[db_name] = {
#         'NAME': os.path.join(settings.BASE_DIR, db_path),
#         'ENGINE': 'django.db.backends.sqlite3'}
#     # Ensure the remaining default connection information is defined.
#     # EDIT: this is actually performed for you in the wrapper class __getitem__
#     # method.. although it may be good to do it when being initially setup to
#     # prevent runtime errors later.
#     # connections.databases.ensure_defaults(db_name)
#     if needs_sync:
#         # Don't import django.core.management if it isn't needed.
#         from django.core.management import call_command
#         print('Building DB structure...')
#         os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SpreadModel.settings")
#         call_command('migrate',
#             # verbosity=0,
#             interactive=False,
#             database=connections[db_name].alias,  # database=self.connection.alias,
#             load_initial_data=False)
#         # call_command('syncdb', )
#         print('Done creating database')
#
#
# def db_save(file_path):
#     create_db_connection('save_file', file_path)
#     top_level_models = [Scenario, Population, Disease, ControlMasterPlan]
#     for parent_object in top_level_models:
#         try:
#             node = parent_object.objects.using('default').get(id=1)
#             node.save(using='save_file')
#         except ObjectDoesNotExist:
#             print("Couldn't find a ", parent_object)
#
#     unsaved_changes(False)  # File is now in sync
#     return 'Scenario Saved'


def workspace_path(target):
    return "./workspace/"+target


def file_list(extension=''):
    db_files = sorted(glob("./workspace/*" + extension), key=lambda s: s.lower())  # alphabetical, no case
    return map(lambda f: os.path.basename(f), db_files)  # remove directory and extension


def file_dialog(request):
    db_files = file_list(".sqlite3")
    context = {'db_files': db_files,
               'title': 'Select a new Scenario to Open'}
    return render(request, 'ScenarioCreator/workspace.html', context)


def save_scenario(request):
    """Save to the existing session of a new file name if target is provided
    """
    target = request.POST['filename']
    scenario_filename(target)
    print('Copying database to', target)
    full_path = workspace_path(target) + ".sqlite3" if target[-8:] != '.sqlite3' else workspace_path(target)
    shutil.copy(activeSession(), full_path)
    unsaved_changes(False)  # File is now in sync
    return redirect('/setup/Scenario/1/')


def update_db_version():
    print("Checking Scenario version")

    print('Building DB structure...')
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SpreadModel.settings")
    call_command('migrate',
                 # verbosity=0,
                 interactive=False,
                 database=connections['scenario_db'].alias,
                 load_initial_data=False)
    print('Done creating database')


def delete_file(request, target):
    print("Deleting", target)
    os.remove(workspace_path(target))
    print("Done")
    return redirect('/setup/Workspace')  # TODO: refresh instead of redirecting


def open_scenario(request, target):
    print("Copying ", workspace_path(target), "to", activeSession())
    shutil.copy(workspace_path(target), activeSession())
    scenario_filename(target)
    print('Sessions overwritten with ', target)
    update_db_version()
    unsaved_changes(False)  # File is now in sync
    # else:
    #     print('File does not exist')
    return redirect('/setup/Scenario/1/')


def new_scenario(request):
    print("Deleting", activeSession())
    try:
        os.remove(activeSession())
    except:
        pass  # the file may not exist anyways
    #creates a new blank file by migrate / syncdb
    call_command('syncdb',
                 # verbosity=0,
                 interactive=False,
                 database=connections['scenario_db'].alias,
                 load_initial_data=False)
    call_command('migrate',
                 # verbosity=0,
                 interactive=False,
                 database=connections['scenario_db'].alias,
                 load_initial_data=False)
    scenario_filename("Untitled Scenario")
    return redirect('/setup/Scenario/1/')


def copy_file(request, target):
    copy_name = re.sub(r'(?P<name>.*)\.(?P<ext>.*)', r'\g<name> - Copy.\g<ext>', target)
    print("Copying ", target, "to", copy_name)
    shutil.copy(workspace_path(target), workspace_path(copy_name))
    return redirect('/setup/Workspace/')


def download_file(request, target):
    file_path = workspace_path(target)
    f = open(file_path, "rb")
    response = HttpResponse(f, content_type="application/x-sqlite")  # TODO: generic content type
    response['Content-Disposition'] = 'attachment; filename="' + target
    return response


def handle_file_upload(request):
    uploaded_file = request.FILES['file']
    filename = uploaded_file._name
    with open(workspace(filename), 'wb+') as destination:
        for chunk in uploaded_file.chunks():
            destination.write(chunk)
    return filename


def upload_scenario(request):
    handle_file_upload(request)
    return redirect('/setup/Workspace/')


def upload_population(request):
    from Settings.models import SmSession
    session = SmSession.objects.get(pk=1)
    if 'GET' in request.method:
        json = '{"status": "%s", "percent": "%s"}' % (session.population_upload_status, session.population_upload_percent*100)
        return HttpResponse(json, content_type="application/json")

    session.set_population_upload_status("Processing file")
    filename = request.POST.get('filename') if 'filename' in request.POST else handle_file_upload(request)
    model = Population(source_file=filename)
    model.save()
    unsaved_changes(True)
    # wait for Population parsing (up to 5 minutes)
    session.reset_population_upload_status()
    return HttpResponse('{"status": "complete", "redirect": "/setup/Populations/"}', content_type="application/json")


def filtering_params(request):
    """Collects the list of parameters to filter by.  Because of the way this is setup:
    1) Only keys mentioned in this list will be used (security, functionality).
    2) Only one filter for each choice key can be used (e.g. only one production_type__name)"""
    params = {}
    keys = ['latitude__gte', 'latitude__eq', 'latitude__lte', 'longitude__gte', 'longitude__eq',
            'longitude__lte', 'initial_size__gte', 'initial_size__eq', 'initial_size__lte',  # 3 permutations for each number field
            'production_type__name', 'initial_state']
    for key in keys:
        if key in request.GET:
            params[key] = request.GET.get(key)
    return params


def filter_info(request, params):
    """Provides the information necessary for Javascript to fully construct a set of filters for Population"""
    info = {}
    # each select option
    info['select_fields'] = {'production_type__name': [x.name for x in ProductionType.objects.all()],
                             'initial_state': Unit.initial_state_choices}
    info['numeric_fields'] = ["latitude","longitude", "initial_size"]
    info['remaining_filters'] = [x for x in info['select_fields'] if x not in params.keys()] #TODO: add numeric_fields
    return info


def population(request):
    """"See also Pagination https://docs.djangoproject.com/en/dev/topics/pagination/"""
    context = {}
    FarmSet = modelformset_factory(Unit, extra=0, form=UnitFormAbbreviated, can_delete=True)
    if save_formset_succeeded(FarmSet, Unit, context, request):
        return redirect(request.path)
    if Population.objects.filter(id=1).exists():
        sort_type = request.GET.get('sort_by', 'initial_state')
        query_filter = Q()
        params = filtering_params(request)
        for key, value in params.items():  # loops through params and stacks filters in an AND fashion
            query_filter = query_filter & Q(**{key: value})
        initialized_formset = FarmSet(queryset=Unit.objects.filter(query_filter).order_by(sort_type)[:30])
        context['formset'] = initialized_formset
        context['filter_info'] = filter_info(request, params)
    else:
        xml_files = file_list(".xml")
        context['xml_files'] = xml_files
    return render(request, 'ScenarioCreator/Population.html', context)


def run_simulation(request):
    #execute system commands here
    return render(request, 'ScenarioCreator/SimulationProgress.html', {})