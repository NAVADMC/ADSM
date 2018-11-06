import re
import os
import shutil
import traceback
from django.conf import settings
from django.db import close_old_connections
from django.http import JsonResponse, HttpRequest
from django.shortcuts import redirect, render, HttpResponse
from django.utils.html import strip_tags
from django.utils.safestring import mark_safe
from ADSMSettings.models import SmSession, unsaved_changes
from ADSMSettings.forms import ImportForm
from ADSMSettings.xml2sqlite import import_naadsm_xml
from ADSMSettings.utils import update_db_version, db_path, workspace_path, db_list, handle_file_upload, graceful_startup, scenario_filename, \
    copy_blank_to_session, create_super_user
from Results.models import outputs_exist
from ScenarioCreator.utils import convert_user_notes_to_unit_id


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
            npu = os.path.join(settings.BASE_DIR, 'npu'+settings.EXTENSION)
            launch_external_program_and_exit(npu, close_self=False, )#cmd_args=['--silent'])  # NPU will force close this
            return HttpResponse("success")
        except:
            print ("Failed to set DB to update!")
            return HttpResponse("failure")


def file_dialog(request):
    context = {'db_files': (db_list()),
               'title': 'Select a new Scenario to Open'}
    return render(request, 'ScenarioCreator/workspace.html', context)


def import_status(request):
    from ADSMSettings.models import SmSession
    session = SmSession.objects.get()
    json_response = {"status": session.population_upload_status}
    return JsonResponse(json_response)


def run_importer(request, new_name=None):
    param_path = handle_file_upload(request, 'parameters_xml', is_temp_file=True, overwrite_ok=True)  # we don't want param XMLs stored next to population XMLs
    popul_path = handle_file_upload(request, 'population_xml', is_temp_file=True, overwrite_ok=True)
    import_legacy_scenario(param_path, popul_path, new_name=new_name)


def import_legacy_scenario(param_path, popul_path, new_name=None):
    if new_name:
        names_without_extensions = new_name
    else:
        names_without_extensions = tuple(
            os.path.splitext(os.path.basename(x))[0] for x in [param_path, popul_path])  # stupid generators...
        names_without_extensions = '%s with %s' % names_without_extensions

    import_naadsm_xml(popul_path, param_path)  # puts all the data in activeSession
    convert_user_notes_to_unit_id()
    scenario_filename(names_without_extensions, check_duplicates=True)
    return save_scenario(None)  # This will overwrite a file of the same name without prompting
    # except BaseException as error:
    #     print("Import process crashed\n", error)
    #     return redirect("/app/ImportScenario/")
    #this could be displayed as a more detailed status screen


def import_naadsm_scenario(request, new_name=None):
    if 'POST' in request.method:
        initialized_form = ImportForm(request.POST, request.FILES)
    else:  # GET page for the first time
        initialized_form = ImportForm()
        close_old_connections()  # close old session
        new_scenario(new_name=new_name)  # add a scenario to session

    context = {'form': initialized_form,
               'title': "Import Legacy NAADSM Scenario in XML format",
               'loading_message': "Please wait as we import your file...",
               'error_title': "Import Error:",
               'base_page': 'ScenarioCreator/crispy-model-form.html',
               }

    if initialized_form.is_valid():
        try:
            run_importer(request, new_name=new_name)
            return loading_screen(request)
        except Exception as e:
            import sys
            info = sys.exc_info()
            # stacktrace = info[3]
            # print(stacktrace)
            # traceback.print_exc()

            print(info)
            print(str(info[2]))
            context['form_errors'] = mark_safe(str(info[1]))
            # go on to serve the form normally with Error messages attached
    else:
        context['form_errors'] = initialized_form.errors
    return render(request, 'ScenarioCreator/MainPanel.html', context)  # render in validation error messages


def upload_scenario(request):
    if '.sqlite' in request.FILES['file']._name or '.db' in request.FILES['file']._name:
        handle_file_upload(request)  #TODO: This can throw an error, but this method isn't used currently
        return redirect('/app/Workspace/')
    else:
        raise ValueError("You can only submit files with '.sqlite' in the file name.")  # ugly error should be caught by Javascript first


def open_scenario(request, target, wrap_target=True):
    if not target.lower().endswith('.db'):
        target = target + ".db"
    if wrap_target:
        target = os.path.join(workspace_path(os.path.splitext(target)[0]), target)
    print("Copying ", target, "to", db_path(), ". This could take several minutes...")
    close_old_connections()
    shutil.copy(target, db_path(name='scenario_db'))
    scenario_filename(os.path.basename(target))
    print('Sessions overwritten with ', target)
    update_db_version()
    convert_user_notes_to_unit_id()
    unsaved_changes(False)  # File is now in sync
    SmSession.objects.all().update(iteration_text = '', simulation_has_started=outputs_exist())  # This is also reset from delete_all_outputs
    # else:
    #     print('File does not exist')
    return redirect('/setup/Scenario/1/')


def open_test_scenario(request, target):
    return open_scenario(request, target, False)


def new_scenario(request=None, new_name=None):
    copy_blank_to_session()

    update_db_version()
    if new_name:
        try:
            scenario_filename(new_name, check_duplicates=True)
        except: pass  # validation may kick it back in which case they'll need to rename it in a file browser
    return redirect('/setup/Scenario/1/')


def save_scenario(request=None):
    """Save to the existing session of a new file name if target is provided
    """
    if request is not None and 'filename' in request.POST and request.POST['filename']:
        target = request.POST['filename']
    else:
        target = scenario_filename()
    target = strip_tags(target)
    full_path = workspace_path(target + "/" + target + ('.db' if not target.endswith('.db') else ''))
    try:
        if '\\' in target or '/' in target:  # this validation has to be outside of scenario_filename in order for open_test_scenario to work
            raise ValueError("Slashes are not allowed: " + target)
        scenario_filename(target)
        print('Copying database to', target)

        if not os.path.exists(os.path.dirname(full_path)):
            os.makedirs(os.path.dirname(full_path))
        shutil.copy(db_path(), full_path)
        unsaved_changes(False)  # File is now in sync
        print('Done Copying database to', full_path)
    except (IOError, AssertionError, ValueError) as err:
        if request is not None:
            save_error = 'Failed to save filename:' + str(err)
            print('Encountered an error while copying file', full_path)
            return render(request, 'ScenarioName.html', {"failure_message": save_error})

    if request is not None and request.is_ajax():
        return render(request, 'ScenarioName.html', {"success_message": "File saved to " + target,
                                                     "filename": scenario_filename(),
                                                     'unsaved_changes': unsaved_changes()})
    else:
        return redirect('/setup/Scenario/1/')


def delete_file(request, target):
    print("Deleting", target)
    if "\\" not in target and os.path.splitext(target)[1].lower() in ['.db', '.sqlite', '.sqlite3']:
        target = os.path.splitext(target)[0]
        shutil.rmtree(workspace_path(target))
    else:
        os.remove(workspace_path(target))
    print("Done")
    return HttpResponse()


def copy_file(request, target, destination):
    if target.replace('.db', '') == scenario_filename():  # copying the active scenario
        return save_scenario(request)
    print("Copying", target, "to", destination, ". This could take several minutes...")
    target = workspace_path(os.path.splitext(target)[0] + "/" + target)
    destination = workspace_path(os.path.splitext(destination)[0] + "/" + destination)
    if not destination.endswith('.db'):
        destination += ".db"
    if not os.path.exists(os.path.dirname(destination)):
        os.makedirs(os.path.dirname(destination))
    shutil.copy(target, destination)
    print("Done copying", target)
    return redirect('/')


def download_file(request):
    target = request.GET['target']
    target = target if target[-1] not in r'/\\' else target[:-1]  # shouldn't be a trailing slash
    if "\\" not in target and os.path.splitext(target)[1].lower() in ['.db', '.sqlite', '.sqlite3']:
        file_path = workspace_path(os.path.splitext(target)[0] + "/" + target)
    else:
        file_path = workspace_path(target)
    f = open(file_path, "rb")
    response = HttpResponse(f, content_type="application/x-sqlite")  # TODO: generic content type
    response['Content-Disposition'] = 'attachment; filename="' + target
    return response


def backend(request, url):
    from django.contrib.auth import login
    from django.contrib.auth.models import User
    user = User.objects.filter(username="ADSM").first()
    if user is None:
        user = create_super_user()
    print(user, user.username)
    if not user.is_superuser:
        user.is_superuser = True
        user.save()
    if not user.is_staff:
        user.is_staff = True
        user.save()
    user.backend = 'django.contrib.auth.backends.ModelBackend'
    login(request, user)
    return redirect(url)


def show_help_text_json(request):
    if 'POST' in request.method:
        new_value = request.POST['show_help_text']
        set_to = new_value == 'true'
        SmSession.objects.all().update(show_help_text=set_to)
        return JsonResponse({'status':'success'})
    else:  # GET
        return JsonResponse({'show_help_text': SmSession.objects.get().show_help_text})


def show_help_overlay_json(request):
    if 'POST' in request.method:
        new_value = request.POST['show_help_overlay']
        set_to = new_value == 'true'
        SmSession.objects.all().update(show_help_overlay=set_to)
        return JsonResponse({'status':'success'})
    else:  # GET
        return JsonResponse({'show_help_overlay': SmSession.objects.get().show_help_overlay})
