import re
import os
import shutil
from django.db import close_old_connections
from django.shortcuts import redirect, render, HttpResponse
from Settings.models import scenario_filename, SmSession, unsaved_changes
from Settings.forms import ImportForm
from Settings.xml2sqlite import import_naadsm_xml
from Settings.utils import update_is_needed, graceful_startup, reset_db, update_db_version, activeSession, workspace_path, file_list, handle_file_upload


def update_adsm_from_git(request):
    """This sets the update_on_startup flag for the next program start."""
    if 'GET' in request.method:
        try:
            session = SmSession.objects.get_or_create(id=1)[0]
            session.update_on_startup = True
            session.save()
            return HttpResponse("success")
        except:
            print ("Failed to set DB to update!")
            return HttpResponse("failure")


def check_update(request):
    graceful_startup()

    session = SmSession.objects.get_or_create(id=1)[0]
    session.update_available = update_is_needed()
    session.save()

    return redirect('/setup/')


def file_dialog(request):
    db_files = file_list(".sqlite3")
    context = {'db_files': db_files,
               'title': 'Select a new Scenario to Open'}
    return render(request, 'ScenarioCreator/workspace.html', context)


def run_importer(request):
    param_path = handle_file_upload(request, 'parameters_xml', is_temp_file=True)  # we don't want param XMLs stored next to population XMLs
    popul_path = handle_file_upload(request, 'population_xml')
    names_without_extensions = tuple(os.path.splitext(os.path.basename(x))[0] for x in [param_path, popul_path])  # stupid generators...
    new_scenario(request)  # I realized this was WAY simpler than creating a new database connection
    import_naadsm_xml(popul_path, param_path)  # puts all the data in activeSession
    scenario_filename('%s with %s' % names_without_extensions)
    return save_scenario(None)  # This will overwrite a file of the same name without prompting
    # except BaseException as error:
    #     print("Import process crashed\n", error)
    #     return redirect("/app/ImportScenario/")
    #this could be displayed as a more detailed status screen
        
    
def import_naadsm_scenario(request):
    if request.method == "POST":
        initialized_form = ImportForm(request.POST, request.FILES)
    else:  # GET page for the first time
        initialized_form = ImportForm()
    if initialized_form.is_valid():
        return run_importer(request)
    context = {'form': initialized_form, 'title': "Import Legacy NAADSM Scenario in XML format"}
    return render(request, 'ScenarioCreator/crispy-model-form.html', context)  # render in validation error messages


def upload_scenario(request):
    if '.sqlite' in request.FILES['file']._name:
        handle_file_upload(request)
        return redirect('/app/Workspace/')
    else:
        raise ValueError("You can only submit files with '.sqlite' in the file name.")  # ugly error should be caught by Javascript first


def open_scenario(request, target):
    print("Copying ", workspace_path(target), "to", activeSession(), ". This could take several minutes...")
    close_old_connections()
    shutil.copy(workspace_path(target), activeSession())
    scenario_filename(target)
    print('Sessions overwritten with ', target)
    update_db_version()
    unsaved_changes(False)  # File is now in sync
    # else:
    #     print('File does not exist')
    return redirect('/setup/Scenario/1/')


def save_scenario(request=None):
    """Save to the existing session of a new file name if target is provided
    """
    if request:
        target = request.POST['filename']
        scenario_filename(target)
    else:
        target = scenario_filename()
    print('Copying database to', target)
    full_path = workspace_path(target) + ('.sqlite3' if target[-8:] != '.sqlite3' else '')
    save_error = None
    try:
        shutil.copy(activeSession(), full_path)
        unsaved_changes(False)  # File is now in sync
        print('Done Copying database to', target)
    except IOError:
        save_error = 'Failed to save file.'
        print('Encountered an error while copying file', target)
    if request is not None and request.is_ajax():
        if save_error:
            json_response = '{"status": "failed", "message": "%s"}' % save_error
        else:
            json_response = '{"status": "success"}'
        return HttpResponse(json_response, content_type="application/json")
    else:
        return redirect('/setup/Scenario/1/')


def delete_file(request, target):
    print("Deleting", target)
    os.remove(workspace_path(target))
    print("Done")
    return HttpResponse()


def copy_file(request, target):
    copy_name = re.sub(r'(?P<name>.*)\.(?P<ext>.*)', r'\g<name> - Copy.\g<ext>', target)
    print("Copying", target, "to", copy_name, ". This could take several minutes...")
    shutil.copy(workspace_path(target), workspace_path(copy_name))
    print("Done copying", target)
    return redirect('/app/Workspace/')


def download_file(request, target):
    file_path = workspace_path(target)
    f = open(file_path, "rb")
    response = HttpResponse(f, content_type="application/x-sqlite")  # TODO: generic content type
    response['Content-Disposition'] = 'attachment; filename="' + target
    return response


def new_scenario(request=None):
    reset_db('scenario_db')
    reset_db('default')
    update_db_version()
    return redirect('/setup/Scenario/1/')
