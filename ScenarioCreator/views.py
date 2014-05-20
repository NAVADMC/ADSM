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
from ScenarioCreator.forms import *  # This is absolutely necessary for dynamic form loading
from Settings.models import SmSession
from django.forms.models import modelformset_factory
from django.forms.models import inlineformset_factory


edge_cases = ['RelationalPoint']

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
    if new_value is not None:  # you can still set it to ''
        session.scenario_filename = new_value
        session.save()
    return session.scenario_filename


def activeSession():
    full_path = settings.DATABASES['scenario_db']['NAME']
    return os.path.basename(full_path)


def simulation_ready_to_run(context):
    context = dict(context)
    # excluded statuses that shouldn't be blocking a simulation run
    for key in ['filename', 'unsaved_changes', 'IndirectSpreads', 'AirborneSpreads', 'ProbabilityFunctions', 'RelationalFunctions']:
        context.pop(key, None)
    return all(context.values())


def basic_context():  # TODO: This might not be performant... but it's nice to have a live status
    PT_count = ProductionType.objects.count()
    context =  {'filename': scenario_filename(),
            'unsaved_changes': unsaved_changes(),
            'Scenario': Scenario.objects.count(),
            'OutputSetting': OutputSettings.objects.count(),
            'Population': Population.objects.count(),
            'ProductionTypes': PT_count,
            'Farms': Unit.objects.count(),
            'Disease': Disease.objects.count(),
            'Progressions': DiseaseProgression.objects.count(),
            'ProgressionAssignment': DiseaseProgressionAssignment.objects.count() == PT_count and PT_count, #Fixed false complete status when there are no Production Types
            'DirectSpreads': DirectSpread.objects.count(),
            'IndirectSpreads': IndirectSpread.objects.count(),
            'AirborneSpreads': AirborneSpread.objects.count(),
            'Transmissions': ProductionTypePairTransmission.objects.count() >= PT_count ** 2 and PT_count, #Fixed false complete status when there are no Production Types
            'ControlMasterPlan': ControlMasterPlan.objects.count(),
            'Protocols': ControlProtocol.objects.count(),
            'ProtocolAssignments': ProtocolAssignment.objects.count(),
            'Zones': Zone.objects.count(),
            'ZoneEffects': ZoneEffectOnProductionType.objects.count(),
            'ProbabilityFunctions': ProbabilityFunction.objects.count(),
            'RelationalFunctions': RelationalFunction.objects.count()}
    context['Simulation'] = simulation_ready_to_run(context)
    return context


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


def disease_spread(request):
    context = basic_context()
    extra_count, missing = extra_forms_needed()
    SpreadSet = modelformset_factory(ProductionTypePairTransmission, extra=extra_count, form=ProductionTypePairTransmissionForm)

    try:
        initialized_formset = SpreadSet(request.POST, request.FILES, queryset=ProductionTypePairTransmission.objects.all())
        if initialized_formset.is_valid():
            instances = initialized_formset.save()
            print(instances)
            unsaved_changes(True)
            return redirect(request.path)  # update these numbers after database save because they've changed
    except ValidationError:
        initialized_formset = SpreadSet(queryset=ProductionTypePairTransmission.objects.all())
    context['formset'] = initialized_formset
    for index, pt in enumerate(missing):
        index += ProductionTypePairTransmission.objects.count()
        context['formset'][index].fields['source_production_type'].initial = pt.id
        context['formset'][index].fields['destination_production_type'].initial = pt.id

    context['title'] = 'How does Disease spread from one Production Type to another?'
    return render(request, 'ScenarioCreator/FormSet.html', context)


def populate_forms_matching_ProductionType(MyFormSet, TargetModel, context, missing, request):
    """FormSet is pre-populated with existing assignments and it detects and fills in missing
    assignments with a blank form with production type filled in."""

    try:
        initialized_formset = MyFormSet(request.POST, request.FILES, queryset=TargetModel.objects.all())
        if initialized_formset.is_valid():
            instances = initialized_formset.save()
            print(instances)
            unsaved_changes(True)
            context['formset'] = initialized_formset
            return False
    except ValidationError:
        forms = MyFormSet(queryset=TargetModel.objects.all())
        for index, pt in enumerate(missing):
            index += TargetModel.objects.count()
            forms[index].fields['production_type'].initial = pt.id
        context['formset'] = forms
    return True


def assign_protocols(request):
    context = basic_context()
    missing = ProductionType.objects.filter(protocolassignment__isnull=True)
    ProtocolSet = modelformset_factory(ProtocolAssignment, extra=len(missing), form=ProtocolAssignmentForm)
    if populate_forms_matching_ProductionType(ProtocolSet, ProtocolAssignment, context, missing, request):
        context['title'] = 'Assign a Control Protocol to each Production Type'
        return render(request, 'ScenarioCreator/FormSet.html', context)
    else:
        return redirect(request.path)


def assign_progressions(request):
    """FormSet is pre-populated with existing assignments and it detects and fills in missing
    assignments with a blank form with production type filled in."""

    context = basic_context()
    missing = ProductionType.objects.filter(diseaseprogressionassignment__isnull=True)
    ProgressionSet = modelformset_factory(DiseaseProgressionAssignment,
                                     extra=len(missing),
                                     form=DiseaseProgressionAssignmentForm)
    if populate_forms_matching_ProductionType(ProgressionSet, DiseaseProgressionAssignment, context, missing, request):
        context['title'] = 'Set what Progression each Production Type has with the Disease'
        return render(request, 'ScenarioCreator/FormSet.html', context)
    else:
        return redirect(request.path)


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
    context = basic_context()
    context = initialize_relational_form(context, primary_key, request)
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
            return redirect('/setup/RelationalFunction/%i/' % created_instance.id)
    context['title'] = "Create a Relational Function"
    return render(request, 'ScenarioCreator/RelationalFunction.html', context)


def save_new_instance(initialized_form, request):
    model_instance = initialized_form.save()  # write to database
    unsaved_changes(True)  # Changes have been made to the database that haven't been saved out to a file
    model_name = model_instance.__class__.__name__
    if request.is_ajax():
        msg = {'pk': model_instance.pk,
               'title': spaces_for_camel_case(str(model_instance)),
               'model': model_name,
               'status': 'success'}
        return HttpResponse(json.dumps(msg), content_type="application/json")
    return redirect('/setup/%s/%i/' % (model_name, model_instance.pk))  # redirect to edit URL


def new_form(request, initialized_form, context):
    if initialized_form.is_valid():
        return save_new_instance(initialized_form, request)
    return render(request, 'ScenarioCreator/crispy-model-form.html', context)  # render in validation error messages


def get_model_name_and_form(request):
    model_name = re.split('\W+', request.path)[2]  # Second word in the URL
    form = globals()[model_name + 'Form']  # IMPORTANT: depends on naming convention
    return model_name, form


def initialize_from_existing_model(primary_key, request):
    """Raises an ObjectDoesNotExist exception when the primary_key is invalid"""
    model_name, form_class = get_model_name_and_form(request)
    model = form_class.Meta.model.objects.get(id=primary_key)  # may raise an exception
    initialized_form = form_class(request.POST or None, instance=model)
    return initialized_form, model_name


'''New / Edit / Copy trio that are called from URLs'''
def new_entry(request):
    model_name, form = get_model_name_and_form(request)
    if model_name == 'RelationalFunction':
        return relational_function(request)
    initialized_form = form(request.POST or None)
    context = basic_context()
    context['form'] = initialized_form
    context['title'] = "Create a new " + spaces_for_camel_case(model_name)
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

    context = basic_context()
    context['form'] = initialized_form
    context['title'] = "Edit a " + spaces_for_camel_case(model_name)
    context['model_link'] = '/setup/' + model_name + '/' + primary_key + '/'
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
    context = basic_context()
    context['form'] = initialized_form
    context['title'] = "Copy a " + spaces_for_camel_case(model_name)
    return render(request, 'ScenarioCreator/crispy-model-form.html', context)


def delete_entry(request, primary_key):
    model_name, form = get_model_name_and_form(request)
    model = form.Meta.model
    model.objects.filter(pk=primary_key).delete()
    return redirect('/setup/%s/new/' % model_name)


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
    return "./workspace/"+target+".sqlite3"
    #os.path.join(BASE_DIR, 'settings.sqlite3')


def file_dialog(request):
    # try:
    # print( "Saving ", scenario_filename())
    # if scenario_filename():
    #     save_scenario(request, scenario_filename())  # Save the file that's already open
    # except ValueError:
    #     pass  # New scenario
    db_files = glob("./workspace/*.sqlite3")
    db_files = map(lambda f: os.path.splitext(os.path.basename(f))[0], db_files)  # remove directory and extension
    context = basic_context()
    context['db_files'] = db_files
    context['title'] = 'Select a new Scenario to Open'
    return render(request, 'ScenarioCreator/workspace.html', context)


def save_scenario(request):
    """Save to the existing session of a new file name if target is provided
    """
    target = request.POST['filename']
    if target:
        scenario_filename(target)
        print('Copying database to', target)
        shutil.copy(activeSession(), workspace_path(target))
        unsaved_changes(False)  # File is now in sync
    else:
        raise ValueError('You need to select a file path to save first')
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


def delete_scenario(request, target):
    print("Deleting", target)
    os.remove(workspace_path(target))
    print("Done")
    return redirect('/setup/Workspace')


def open_scenario(request, target):
    # if os.path.isfile(workspace_path(target)):
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


def copy_scenario(request, target):
    copy_name = target + ' - Copy'  #re.sub(r'(.*)\.sqlite3', r'\6 - Copy\.sqlite3', target)
    print("Copying ", target, "to", copy_name)
    shutil.copy(workspace_path(target), workspace_path(copy_name))
    return redirect('/setup/Workspace/')


def download_scenario(request, target):
    file_path = workspace_path(target)
    f = open(file_path, "rb")
    response = HttpResponse(f, content_type="application/x-sqllite")
    response['Content-Disposition'] = 'attachment; filename="' + target + '.sqlite3"'
    return response


def upload_scenario(request):
    uploaded_file = request.FILES['file']
    filename = uploaded_file._name
    with open(workspace(filename), 'wb+') as destination:
        for chunk in uploaded_file.chunks():
            destination.write(chunk)
    return redirect('/setup/Workspace/')


def run_simulation(request):
    #execute system commands here
    return render(request, 'ScenarioCreator/SimulationProgress.html', basic_context())