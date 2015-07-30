import re
import os
import shutil
from django.conf import settings
from django.db import close_old_connections
from django.http import JsonResponse, HttpRequest
from django.shortcuts import redirect, render, HttpResponse
from django.utils.html import strip_tags
from ADSMSettings.models import SmSession, unsaved_changes
from ADSMSettings.forms import ImportForm
from ADSMSettings.xml2sqlite import import_naadsm_xml
from ADSMSettings.utils import reset_db, update_db_version, db_path, workspace_path, file_list, handle_file_upload, graceful_startup, scenario_filename, \
    npu_update_info
from Results.models import outputs_exist


def home(request):
    return redirect('/LoadingScreen/?loading_url=/app/Startup/')


def startup(request):
    graceful_startup()
    return redirect('/setup/Scenario/1/')


def loading_screen(request):
    """Display a loading screen then immediate GET the redirect_url from javascript.
    Just add /?loading_url= to the beginning of any URL"""
    # context processor does not run on this url
    try:
        context = {'loading_url': request.GET['loading_url']}
    except:
        context = {'loading_url': '/setup/Scenario/1/'}
    return render(request, "LoadingScreen.html", context)


def update_adsm_from_git(request):
    from ADSMSettings.utils import launch_external_program_and_exit
    """This sets the update_on_startup flag for the next program start."""
    if 'GET' in request.method:
        try:
            npu = os.path.join(settings.BASE_DIR, 'npu.exe')  # TODO Windows specific
            launch_external_program_and_exit(npu, close_self=False, )#cmd_args=['--silent'])  # NPU will force close this
            return HttpResponse("success")
        except:
            print ("Failed to set DB to update!")
            return HttpResponse("failure")


def file_dialog(request):
    context = {'db_files': (file_list(".sqlite3")),
               'title': 'Select a new Scenario to Open'}
    return render(request, 'ScenarioCreator/workspace.html', context)


def run_importer(request):
    param_path = handle_file_upload(request, 'parameters_xml', is_temp_file=True, overwrite_ok=True)  # we don't want param XMLs stored next to population XMLs
    popul_path = handle_file_upload(request, 'population_xml', is_temp_file=True, overwrite_ok=True)
    import_legacy_scenario(param_path, popul_path)


def import_legacy_scenario(param_path, popul_path):
    names_without_extensions = tuple(os.path.splitext(os.path.basename(x))[0] for x in [param_path, popul_path])  # stupid generators...
    new_scenario()  # I realized this was WAY simpler than creating a new database connection
    import_naadsm_xml(popul_path, param_path)  # puts all the data in activeSession
    scenario_filename('%s with %s' % names_without_extensions, check_duplicates=True)
    return save_scenario(None)  # This will overwrite a file of the same name without prompting
    # except BaseException as error:
    #     print("Import process crashed\n", error)
    #     return redirect("/app/ImportScenario/")
    #this could be displayed as a more detailed status screen
        
    
def import_naadsm_scenario(request):
    if 'POST' in request.method:
        initialized_form = ImportForm(request.POST, request.FILES)
    else:  # GET page for the first time
        initialized_form = ImportForm()
    if initialized_form.is_valid():
        run_importer(request)
        return redirect('/')
    context = {'form': initialized_form, 
               'title': "Import Legacy NAADSM Scenario in XML format", 
               'base_page': 'ScenarioCreator/crispy-model-form.html'}
    return render(request, 'ScenarioCreator/navigationPane.html', context)  # render in validation error messages


def upload_scenario(request):
    if '.sqlite' in request.FILES['file']._name:
        handle_file_upload(request)  #TODO: This can throw an error, but this method isn't used currently
        return redirect('/app/Workspace/')
    else:
        raise ValueError("You can only submit files with '.sqlite' in the file name.")  # ugly error should be caught by Javascript first


def open_scenario(request, target, wrap_target=True):
    if wrap_target:
        target = workspace_path(target)
    print("Copying ", target, "to", db_path(), ". This could take several minutes...")
    close_old_connections()
    shutil.copy(target, db_path(name='scenario_db'))
    scenario_filename(os.path.basename(target))
    print('Sessions overwritten with ', target)
    update_db_version()
    unsaved_changes(False)  # File is now in sync
    SmSession.objects.all().update(iteration_text = '', simulation_has_started=outputs_exist())  # This is also reset from delete_all_outputs
    # else:
    #     print('File does not exist')
    return redirect('/setup/Scenario/1/')


def open_test_scenario(request, target):
    return open_scenario(request, target, False)


def save_scenario(request=None):
    """Save to the existing session of a new file name if target is provided
    """
    if request is not None and 'filename' in request.POST:
        target = request.POST['filename']
    else:
        target = scenario_filename()
    target = strip_tags(target)
    full_path = workspace_path(target) + ('.sqlite3' if not target.endswith('.sqlite3') else '')
    try:
        if '\\' in target or '/' in target:  # this validation has to be outside of scenario_filename in order for open_test_scenario to work
            raise ValueError("Slashes are not allowed: " + target)
        scenario_filename(target)
        print('Copying database to', target)

        shutil.copy(db_path(), full_path)
        unsaved_changes(False)  # File is now in sync
        print('Done Copying database to', full_path)
    except (IOError, AssertionError, ValueError) as err:
        if request is not None:
            save_error = 'Failed to save filename:' + str(err)
            print('Encountered an error while copying file', full_path)
            return render(request, 'ScenarioName.html', {"failure_message": save_error})

    if request is not None and request.is_ajax():
        return render(request, 'ScenarioName.html', {"success_message": "File saved to " + target})
    else:
        return redirect('/setup/Scenario/1/')


def delete_file(request, target):
    print("Deleting", target)
    os.remove(workspace_path(target))
    print("Done")
    return HttpResponse()


def copy_file(request, target, destination):
    if target.replace('.sqlite3', '') == scenario_filename():  # copying the active scenario
        return save_scenario(request)
    if not destination.endswith('.sqlite3'):
        destination += ".sqlite3"
    print("Copying", target, "to", destination, ". This could take several minutes...")
    shutil.copy(workspace_path(target), workspace_path(destination))
    print("Done copying", target)
    return redirect('/')


def download_file(request):
    target = request.GET['target']
    target = target if target[-1] not in r'/\\' else target[:-1]  # shouldn't be a trailing slash
    file_path = workspace_path(target)
    f = open(file_path, "rb")
    response = HttpResponse(f, content_type="application/x-sqlite")  # TODO: generic content type
    response['Content-Disposition'] = 'attachment; filename="' + target
    return response


def new_scenario(request=None, new_name=None):
    reset_db('scenario_db')
    reset_db('default')
    update_db_version()
    if new_name:
        try:
            scenario_filename(new_name, check_duplicates=True)
        except: pass # validation may kick it back in which case they'll need to rename it in a file browser
    return redirect('/setup/Scenario/1/')


def backend(request):
    from django.contrib.auth import login
    from django.contrib.auth.models import User
    user = User.objects.filter(is_staff=True).first()
    print(user, user.username)
    user.backend = 'django.contrib.auth.backends.ModelBackend'
    login(request, user)
    return redirect('/admin/')


def handler500(request):
    print("Caught the error")
    return render(request, '500.html', {})
    #return render_to_response('../templates/error/500.html', {'exception': ex}, context_instance=RequestContext(request), status=404)
