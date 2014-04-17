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
from django.forms.models import inlineformset_factory
from django.forms.models import modelformset_factory


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


def basic_context():  # TODO: This might not be performant... but it's nice to have a live status
    PT_count = ProductionType.objects.count()
    return {'filename': scenario_filename(),
            'unsaved_changes': unsaved_changes(),
            'Scenario': Scenario.objects.count(),
            'OutputSetting': OutputSettings.objects.count(),
            'Population': Population.objects.count(),
            'ProductionTypes': PT_count,
            'Farms': Unit.objects.count(),
            'Disease': Disease.objects.count(),
            'Reactions': DiseaseReaction.objects.count(),
            'ReactionAssignment': DiseaseReactionAssignment.objects.count() == PT_count,
            'DirectSpreads': DirectSpreadModel.objects.count(),
            'IndirectSpreads': IndirectSpreadModel.objects.count(),
            'AirborneSpreads': AirborneSpreadModel.objects.count(),
            'Transmissions': ProductionTypePairTransmission.objects.count() == PT_count ** 2,
            'ControlMasterPlan': ControlMasterPlan.objects.count(),
            'Protocols': ControlProtocol.objects.count(),
            'ProtocolAssignments': ProtocolAssignment.objects.count(),
            'Zones': Zone.objects.count(),
            'ZoneEffects': ZoneEffectOnProductionType.objects.count(),
            'ProbabilityFunctions': ProbabilityFunction.objects.count(),
            'RelationalFunctions': RelationalFunction.objects.count()}


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
            return redirect('/setup/DiseaseSpread/')  # update these numbers after database save because they've changed
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
    except ValidationError:
        forms = MyFormSet(queryset=TargetModel.objects.all())
        for index, pt in enumerate(missing):
            index += TargetModel.objects.count()
            forms[index].fields['production_type'].initial = pt.id
        context['formset'] = forms


def assign_protocols(request):
    context = basic_context()
    missing = ProductionType.objects.filter(protocolassignment__isnull=True)
    ProtocolSet = modelformset_factory(ProtocolAssignment, extra=len(missing), form=ProtocolAssignmentForm)
    populate_forms_matching_ProductionType(ProtocolSet, ProtocolAssignment, context, missing, request)

    context['title'] = 'Assign a Control Protocol to each Production Type'
    return render(request, 'ScenarioCreator/FormSet.html', context)


def assign_reactions(request):
    """FormSet is pre-populated with existing assignments and it detects and fills in missing
    assignments with a blank form with production type filled in."""

    context = basic_context()
    missing = ProductionType.objects.filter(diseasereactionassignment__isnull=True)
    ReactionSet = modelformset_factory(DiseaseReactionAssignment,
                                     extra=len(missing),
                                     form=DiseaseReactionAssignmentForm)
    populate_forms_matching_ProductionType(ReactionSet, DiseaseReactionAssignment, context, missing, request)

    context['title'] = 'Set what Reaction each Production Type has to the Disease'
    return render(request, 'ScenarioCreator/FormSet.html', context)


def save_new_instance(initialized_form, request):
    model_instance = initialized_form.save()  # write to database
    unsaved_changes(True)  # Changes have been made to the database that haven't been saved out to a file
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
        unsaved_changes(True)  # Changes have been made to the database that haven't been saved out to a file

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
