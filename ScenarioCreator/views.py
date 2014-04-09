from glob import glob
import json
import os
import shutil
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.db import connections
from django.conf import settings
import re
from ScenarioCreator.forms import *  # This is absolutely necessary for dynamic form loading
from Settings.models import SmSession


def scenario_filename(new_value=None):
    session = SmSession.objects.get_or_create(id=1)[0]  # This keeps track of the state for all views and is used by basic_context
    if new_value is not None:  # you can still set it to ''
        session.scenario_filename = new_value
        session.save()
    return session.scenario_filename


def activeSession():
    full_path = settings.DATABASES['scenario_db']['NAME']
    return os.path.split(full_path)[-1]


def basic_context():  # TODO: This might not be performant... but it's nice to have a live status
    return {'filename': scenario_filename(),
            'Scenario': Scenario.objects.count(),
            'OutputSetting': OutputSettings.objects.count(),
            'Population': Population.objects.count(),
            'ProductionTypes': ProductionType.objects.count(),
            'Farms': Unit.objects.count(),
            'Disease': Disease.objects.count(),
            'Reactions': DiseaseReaction.objects.count(),
            'DirectSpreads': DirectSpreadModel.objects.count(),
            'IndirectSpreads': IndirectSpreadModel.objects.count(),
            'AirborneSpreads': AirborneSpreadModel.objects.count(),
            'Transmissions': ProductionTypePairTransmission.objects.count(),
            'ControlMasterPlan': ControlMasterPlan.objects.count(),
            'Protocols': ControlProtocol.objects.count(),
            'Zones': Zone.objects.count(),
            'ZoneEffects': ZoneEffectOnProductionType.objects.count()}


def home(request):
    return redirect('/setup/Scenario/1/')


def disease_spread(request):
    context = basic_context()
    forms = []
    pts = list(ProductionType.objects.all())
    for source in pts:
        for destination in pts:
            initialized_form = ProductionTypePairTransmissionForm(request.POST or None)
            initialized_form.fields['source_production_type'].initial = source.id
            initialized_form.fields['destination_production_type'].initial = destination.id
            forms.append(initialized_form)
    context['forms'] = forms
    context['title'] = 'How does Disease spread from one Production Type to another?'
    return render(request, 'ScenarioCreator/ProtocolAssignment.html', context)
    # return render(request, 'ScenarioCreator/DiseaseSpread.html', basic_context())


def assign_protocols(request):
    context = basic_context()
    forms = []
    for pt in ProductionType.objects.all():
        initialized_form = ProtocolAssignmentForm(request.POST or None)
        initialized_form.fields['production_type'].initial = pt.id
        forms.append(initialized_form)
    context['forms'] = forms
    context['title'] = 'Assign a Control Protocol to each Production Type'
    return render(request, 'ScenarioCreator/ProtocolAssignment.html', context)


def assign_reactions(request):
    context = basic_context()
    forms = []
    for pt in ProductionType.objects.all():
        initialized_form = DiseaseReactionAssignmentForm(request.POST or None)
        initialized_form.fields['production_type'].initial = pt.id
        forms.append(initialized_form)
    context['forms'] = forms
    context['title'] = 'Set what Reaction each Production Type has to the Disease'
    return render(request, 'ScenarioCreator/ProtocolAssignment.html', context)


def save_new_instance(initialized_form, request):
    model_instance = initialized_form.save()  # write to database
    model_name = model_instance.__class__.__name__
    if request.is_ajax():
        msg = {'pk': model_instance.pk, 'title': str(model_instance), 'model': model_name, 'status': 'success'}
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
    initialized_form = form(request.POST or None)
    context = basic_context()
    context.update({'form': initialized_form,
                    'title': "Create a new " + model_name})
    return new_form(request, initialized_form, context)


def edit_entry(request, primary_key):
    model_name, form = get_model_name_and_form(request)
    try:
        initialized_form, model_name = initialize_from_existing_model(primary_key, request)
    except ObjectDoesNotExist:
        return redirect('/setup/%s/new/' % model_name)
    if initialized_form.is_valid() and request.method == 'POST':
        initialized_form.save()  # write instance updates to database
    context = basic_context()
    context.update({'form': initialized_form,
                    'title': "Edit a " + model_name}.items())
    return render(request, 'ScenarioCreator/crispy-model-form.html', context)


def copy_entry(request, primary_key):
    model_name, form = get_model_name_and_form(request)
    try:
        initialized_form, model_name = initialize_from_existing_model(primary_key, request)
    except ObjectDoesNotExist:
        return redirect('/setup/%s/new/' % model_name)
    if initialized_form.is_valid() and request.method == 'POST':
        initialized_form.instance.pk = None  # This will cause a new instance to be created
        return save_new_instance(initialized_form, request)
    context = basic_context()
    context.update({'form': initialized_form,
                    'title': "Copy a " + model_name}.items())
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
#     return 'Scenario Saved'


def workspace_path(target):
    return "./workspace/"+target+".sqlite3"


def file_dialog(request):
    # try:
    print( "Saving ", scenario_filename())
    if scenario_filename():
        save_scenario(request, scenario_filename())  # Save the file that's already open
    # except ValueError:
    #     pass  # New scenario
    db_files = glob("./workspace/*.sqlite3")
    db_files = map(lambda x: x.replace('./workspace\\', '').replace('.sqlite3', ''), db_files)
    context = basic_context()
    context['db_files'] = db_files
    context['title'] = 'Select a new Scenario to Open'
    return render(request, 'ScenarioCreator/workspace.html', context)


def save_scenario(request, target=None):
    """Save to the existing session of a new file name if target is provided
    """
    if not target and scenario_filename():
        target = scenario_filename()

    if target:
        scenario_filename(target)
        print('Copying database to', target)
        shutil.copy(activeSession(), workspace_path(target))
    else:
        raise ValueError('You need to select a file path to save first')
    return redirect('/setup/Scenario/1/')


def update_db_version():
    print("Checking Scenario version")
    # Don't import django.core.management if it isn't needed.
    from django.core.management import call_command

    print('Building DB structure...')
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SpreadModel.settings")
    call_command('migrate',
                 # verbosity=0,
                 interactive=False,
                 database=connections['scenario_db'].alias,  # database=self.connection.alias,
                 load_initial_data=False)
    print('Done creating database')


def open_scenario(request, target):
    # if os.path.isfile(workspace_path(target)):
    print("Copying ", workspace_path(target), "to", activeSession())
    shutil.copy(workspace_path(target), activeSession())
    scenario_filename(target)
    print('Sessions overwritten with ', target)
    update_db_version()
    # else:
    #     print('File does not exist')
    return redirect('/setup/Scenario/1/')
