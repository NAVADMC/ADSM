from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import
from future.builtins import open
from future.builtins import map
from future.builtins import str
from future import standard_library
standard_library.install_hooks()

import subprocess
import json
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.forms.models import modelformset_factory
from django.db.models import Q

from Results.models import *  # This is absolutely necessary for dynamic form loading
from ScenarioCreator.forms import *  # This is absolutely necessary for dynamic form loading
from Settings.models import unsaved_changes
from Settings.views import graceful_startup, file_list, handle_file_upload, workspace_path
from Settings.views import adsm_executable_command




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


def add_breadcrumb_context(context, model_name, primary_key=None):
    context['pretty_name'] = spaces_for_camel_case(promote_to_abstract_parent(model_name))
    if model_name not in singletons:
        context['model_link'] = '/setup/' + model_name + '/'
        if primary_key is not None:
            context['model_link'] += primary_key + '/'
    else:  # for singletons, don't list the specific name, just the type
        context['title'] = 'Edit the ' + spaces_for_camel_case(model_name)


def home(request):
    return redirect('/setup/Scenario/1/')


def extra_forms_needed():
    missing = list(ProductionType.objects.all())
    for entry in DiseaseSpreadAssignment.objects.all():
        if entry.destination_production_type_id == entry.source_production_type_id:  #Spread within a species
            missing.remove(entry.source_production_type)
    extra_count = len(missing)
    if not missing and DiseaseSpreadAssignment.objects.count() < ProductionType.objects.count() ** 2:
        #all possible interactions are not accounted for
        extra_count = 1  # add one more blank possibility
    return extra_count, missing


def include_spread(request):
    master = Disease.objects.get_or_create(pk=1)[0]
    if 'GET' in request.method:
        info = {'include_direct_contact_spread': master.include_direct_contact_spread,
                'include_indirect_contact_spread': master.include_indirect_contact_spread,
                'include_airborne_spread': master.include_airborne_spread}
        return HttpResponse(json.dumps(info), content_type="application/json")
    else:  # POST means change
        fields = ['include_direct_contact_spread', 'include_indirect_contact_spread', 'include_airborne_spread']
        for field in fields:
            setattr(master, field, request.POST.get(field) == 'true')
        master.save()
        return HttpResponse('success')  # We don't need to return any data
        

def production_type_permutations():
    spread_assignments = []
    pts = list(ProductionType.objects.all())
    for source in pts:
        for destination in pts:
            spread_assignments.append(DiseaseSpreadAssignment.objects.get_or_create(
                source_production_type=source, destination_production_type=destination)[0])  # first index is object
    return spread_assignments


def assign_disease_spread(request):
    assignment_set = production_type_permutations()
    SpreadSet = modelformset_factory(DiseaseSpreadAssignment, extra=0, form=DiseaseSpreadAssignmentForm)
    try:
        initialized_formset = SpreadSet(request.POST, request.FILES, queryset=DiseaseSpreadAssignment.objects.all())
        if initialized_formset.is_valid():
            instances = initialized_formset.save()
            print(instances)
            return redirect(request.path)  # update these numbers after database save because they've changed

    except ValidationError:
        initialized_formset = SpreadSet(queryset=DiseaseSpreadAssignment.objects.all())
    context = {'formset': initialized_formset,
               'title': 'How does Disease spread from one Production Type to another?'}
    return render(request, 'ScenarioCreator/AssignSpread.html', context)


def zone_effects(request):
    grid_forms = []
    for pt in ProductionType.objects.all():
        row = [pt.name, [] ]  # label and empty list
        for zone in Zone.objects.all():
            instance = ZoneEffectAssignment.objects.get_or_create(production_type=pt, zone=zone)[0]
            form = ZoneEffectAssignmentForm(instance=instance)
            setattr(form, 'pk', instance.pk)  # adding the pk so the javascript can call back
            row[1].append(form)
        grid_forms.append(row)
        

    context = {'grid_forms': grid_forms,
               'title': 'What Effect does a Zone have on each Production Type?',
               'zones': Zone.objects.all()}
    return render(request, 'ScenarioCreator/ZoneEffectGrid.html', context)


def save_formset_succeeded(MyFormSet, TargetModel, context, request):
    try:
        initialized_formset = MyFormSet(request.POST, request.FILES, queryset=TargetModel.objects.all())
        if initialized_formset.is_valid():
            instances = initialized_formset.save()
            print(instances)
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


def collect_backlinks(model_instance):
    from django.contrib.admin.util import NestedObjects
    collector = NestedObjects(using='scenario_db')  # or specific database
    collector.collect([model_instance])
    dependants = collector.nested()  # fun fact: spelling differs between America and Brittain
    print("Found related models:", dependants)
    links = {}
    if len(dependants[1:]):
        for direct_reference in dependants[1:][0]:  # only iterates over the top level
            if not isinstance(direct_reference, list) and not isinstance(direct_reference, RelationalPoint):  # Points are obvious, don't include them
                name = direct_reference.__class__.__name__
                try:  # not everything has a name attr
                    links[str(direct_reference)] = '/setup/%s/%i/' % (name, direct_reference.pk)
                except:
                    links['%s:%i' % (name, direct_reference.pk)] = \
                        '/setup/%s/%i/' % (name, direct_reference.pk)
    print(links)
    return links


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
    context['backlinks'] = collect_backlinks(model)
    context['deletable'] = 'delete/'
    return context


def deepcopy_points(request, primary_key, created_instance):
    queryset = RelationalPoint.objects.filter(relational_function_id=primary_key)
    for point in queryset:  # iterating over points already in DB
        point = RelationalPoint(relational_function=created_instance, x=point.x, y=point.y) # copy with new parent
        point.save()  # This assumes that things in the database are already valid, so doesn't call is_valid()
    queryset = RelationalPoint.objects.filter(relational_function_id=created_instance.id)
    formset = PointFormSet(queryset=queryset) # this queryset does not include anything the user typed in, during the copy operation
    return formset


def initialize_points_from_csv(request):
    import csv  # TODO this SHOULD be the 3.3 version from python-future.org...
    filename = handle_file_upload(request)
    with open(workspace_path(filename)) as csvfile:
        dialect = csv.Sniffer().sniff(csvfile.read(1024))
        csvfile.seek(0)
        header = csv.Sniffer().has_header(csvfile.read(1024))
        csvfile.seek(0)
        if header:
            header = None  #DictReader will pull it off the first line
        else:
            header = ['x', 'y']
        reader = csv.DictReader(csvfile, fieldnames=header, dialect=dialect)
        #TODO: lower case the user provided header
        entries = [line for line in reader]  # ordered list
        initial_values = {}
        for index, point in enumerate(entries):
            initial_values['relationalpoint_set-%i-id' % index] = ''
            initial_values['relationalpoint_set-%i-relational_function' % index] = ''
            initial_values['relationalpoint_set-%i-x' % index] = point['x']
            initial_values['relationalpoint_set-%i-y' % index] = point['y']
        initial_values['relationalpoint_set-TOTAL_FORMS'] = str(len(entries))
        initial_values['relationalpoint_set-INITIAL_FORMS'] = '0'
        initial_values['relationalpoint_set-MAX_NUM_FORMS'] = '1000'
        request.POST.update(initial_values)
    try:
        os.remove(workspace_path(filename))  # we don't want to keep these files around in the workspace
    except: pass  # possible that file was never created
    return request


def relational_function(request, primary_key=None, doCopy=False):
    """This handles the edge case of saving, copying, and creating Relational Functions.  RFs are different from any
    other model in ADSM in that they have a list of RelationalPoints.  These points are listed alongside the normal form.
    Rendering this page means render a form, then a formset of points.  Saving is more complex because the points also
    foreignkey back to the RelationalFunction which must be created before it can be referenced.

    It is possible to integrate this code back into the standard new / edit / copy views by checking for
    context['formset'].  The extra logic for formsets could be kicked in only when one or more formsets are present. At
    the moment integration looks like a bad idea because it would mangle the happy path for the sake of one edge case."""
    context = initialize_relational_form({}, primary_key, request)
    if 'file' in request.FILES:  # data file is present
        request = initialize_points_from_csv(request)
    context['formset'] = PointFormSet(request.POST or None, instance=context['model'])
    if context['form'].is_valid():
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
    add_breadcrumb_context(context, "RelationalFunction")
    return render(request, 'ScenarioCreator/RelationalFunction.html', context)


def ajax_success(model_instance, model_name):
    msg = {'pk': model_instance.pk,
           'title': spaces_for_camel_case(str(model_instance)),
           'model': model_name,
           'status': 'success'}
    return HttpResponse(json.dumps(msg), content_type="application/json")


def save_new_instance(initialized_form, request):
    model_instance = initialized_form.save()  # write to database
    model_name = model_instance.__class__.__name__
    if request.is_ajax():
        return ajax_success(model_instance, model_name)
    if model_name in singletons:
        return redirect('/setup/%s/1/' % model_name)
    return redirect('/setup/%s/' % model_name)  # redirect to list URL


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
    model = globals()[model_name]  # IMPORTANT: depends on import *
    return model_name, model


def initialize_from_existing_model(primary_key, request):
    """Raises an ObjectDoesNotExist exception when the primary_key is invalid"""
    model_name, form_class = get_model_name_and_form(request)
    model = form_class.Meta.model.objects.get(id=primary_key)  # may raise an exception
    initialized_form = form_class(request.POST or None, instance=model)
    return initialized_form, model_name


'''New / Edit / Copy / Delete / List that are called from model generated URLs'''
def new_entry(request, second_try=False):
    model_name, form = get_model_name_and_form(request)
    if model_name == 'RelationalFunction':
        return relational_function(request)
    initialized_form = form(request.POST or None)
    context = {'form': initialized_form, 'title': "Create a new " + spaces_for_camel_case(model_name)}
    add_breadcrumb_context(context, model_name)
    try:
        return new_form(request, initialized_form, context)
    except OperationalError:
        if not second_try:
            graceful_startup()
            return new_entry(request, True)
        return new_form(request, initialized_form, context)


def edit_entry(request, primary_key):
    model_name, form = get_model_name_and_form(request)
    if model_name == 'RelationalFunction':
        return relational_function(request, primary_key)

    try:
        initialized_form, model_name = initialize_from_existing_model(primary_key, request)
    except (ObjectDoesNotExist, OperationalError):
        return redirect('/setup/%s/new/' % model_name)
    if initialized_form.is_valid() and request.method == 'POST':
        model_instance = initialized_form.save()  # write instance updates to database
        if request.is_ajax():
            return ajax_success(model_instance, model_name)

    context = {'form': initialized_form,
               'title': str(initialized_form.instance)}
    add_breadcrumb_context(context, model_name, primary_key)

    if model_name == 'ProbabilityFunction':
        context['backlinks'] = collect_backlinks(initialized_form.instance)
        context['deletable'] = 'delete/'

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
    model.objects.get(pk=primary_key).delete()
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


def upload_population(request):
    from Settings.models import SmSession
    from xml.etree.ElementTree import ParseError
    session = SmSession.objects.get_or_create(pk=1)[0]
    if 'GET' in request.method:
        json = '{"status": "%s", "percent": "%s"}' % (session.population_upload_status, session.population_upload_percent*100)
        return HttpResponse(json, content_type="application/json")

    session.set_population_upload_status("Processing file")
    filename = request.POST.get('filename') if 'filename' in request.POST else handle_file_upload(request)
    model = Population(source_file=workspace_path(filename))
    try:
        model.save()
    except (EOFError, ParseError) as e:
        return HttpResponse('{"status": "failed", "message": "%s"}' % e, content_type="application/json")
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
        context['deletable'] = '/setup/Population/1/delete/'
    else:
        xml_files = file_list(".xml")
        context['xml_files'] = xml_files
    return render(request, 'ScenarioCreator/Population.html', context)


def whole_scenario_validation():
    fatal_errors = []
    for pt in ProductionType.objects.all():
        count = DiseaseProgressionAssignment.objects.filter(production_type=pt, progression__isnull=False).count()
        if not count:
            fatal_errors.append(pt.name + " has no Disease Progression assigned and so is a non-participant in the simulation.")
        count = DiseaseSpreadAssignment.objects.filter(source_production_type=pt, 
                                                              destination_production_type=pt,
                                                              direct_contact_spread__isnull=False).count()
        if not count:
            fatal_errors.append(pt.name + " cannot spread disease from one animal to another, because Direct Spread %s -> %s has not been assigned." % (pt.name, pt.name))
    if not Disease.objects.get_or_create().include_direct_contact_spread:
        fatal_errors.append("Direct Spread is not enabled in this Simulation.")
    return fatal_errors


def validate_scenario(request):
    simulation = subprocess.Popen(adsm_executable_command() + ['--dry-run'],
                                  shell=True,
                                  stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE)
    stdout, stderr = simulation.communicate()  # still running while we work on python validation
    
    fatal_errors = whole_scenario_validation()
    simulation.wait()  # simulation will process db then exit
    print("Return code", simulation.returncode)
    context = {'dry_run_passed': simulation.returncode == 0 and not stderr,
               'sim_output': stdout + stderr,
               'fatal_errors': fatal_errors}
    return render(request, 'ScenarioCreator/Validation.html', context)
