from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from future import standard_library
standard_library.install_hooks()

import re
import os
import platform
import shutil
from glob import glob
import subprocess
from django.shortcuts import redirect, render, HttpResponse
from django.core.management import call_command
from django.db import connections, close_old_connections
from django.conf import settings
from django.db import OperationalError
from ScenarioCreator.models import ZoneEffect
from Settings.models import scenario_filename, SmSession, unsaved_changes
from Settings.utils import close_all_connections

from git.git import git


def activeSession(name='scenario_db'):
    full_path = settings.DATABASES[name]['NAME']
    return os.path.basename(full_path)


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


def update_is_needed():
    try:
        os.chdir(settings.BASE_DIR)
        command = git + ' remote update'
        subprocess.call(command, shell=True)
        command = git + ' status -uno'
        status = subprocess.check_output(command, shell=True)
        print(status)
        return 'is behind' in status
    except:
        print ("Failed in checking if an update is required!")
        return False


def reset_db(name):
    """ It now checks if the file exists.  This will throw a PermissionError if the user has the DB open in another program."""
    print("Deleting", activeSession(name))
    close_old_connections()
    if os.path.exists(activeSession(name)):
        connections[name].close()
        os.remove(activeSession(name))
    else:
        print(activeSession(name), "does not exist")
    #creates a new blank file by migrate / syncdb
    call_command('syncdb',
                 # verbosity=0,
                 interactive=False,
                 database=connections[name].alias,
                 load_initial_data=False)
    if name == 'default':  # create super user
        from django.contrib.auth.models import User
        u = User(username='ADSM', is_superuser=True, is_staff=True)
        u.set_password('ADSM')
        u.save()


def update_db_version():
    print("Checking Scenario version")
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SpreadModel.settings")
    try:
        call_command('migrate',
                     # verbosity=0,
                     interactive=False,
                     database=connections['scenario_db'].alias,
                     load_initial_data=False)
    except:
        print("Error: Migration failed.")
    print('Done creating database')


def graceful_startup():
    """Checks something inside of each of the database files to see if it's valid.  If not, rebuild the database."""
    try:
        SmSession.objects.get_or_create()[0].update_available
    except OperationalError:
        reset_db('default')
    try:
        ZoneEffect.objects.count()
    except OperationalError:
        reset_db('scenario_db')
        update_db_version()


def check_update(request):
    graceful_startup()

    session = SmSession.objects.get_or_create(id=1)[0]
    session.update_available = update_is_needed()
    session.save()

    return redirect('/setup/')


def workspace_path(target):
    if '/' in target or '\\' in target:
        parts = re.split(r'/+\\+', target)  # the slashes here are coming in from URL so they probably don't match os.path.split()
        return os.path.join("workspace", *parts)
    return os.path.join("workspace", target)


def file_list(extension=''):
    db_files = sorted(glob("./workspace/*" + extension), key=lambda s: s.lower())  # alphabetical, no case
    return map(lambda f: os.path.basename(f), db_files)  # remove directory and extension


def file_dialog(request):
    db_files = file_list(".sqlite3")
    context = {'db_files': db_files,
               'title': 'Select a new Scenario to Open'}
    return render(request, 'ScenarioCreator/workspace.html', context)


def handle_file_upload(request):
    uploaded_file = request.FILES['file']
    filename = uploaded_file._name
    with open(workspace_path(filename), 'wb+') as destination:
        for chunk in uploaded_file.chunks():
            destination.write(chunk)
    return filename


def upload_scenario(request):
    if '.sqlite' in request.FILES['file']._name:
        handle_file_upload(request)
        return redirect('/app/Workspace/')
    else:
        raise ValueError("You can only submit files with '.sqlite' in the file name.")  # ugly error should be caught by Javascript first


def open_scenario(request, target):
    print("Copying ", workspace_path(target), "to", activeSession())
    close_all_connections()
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
    except IOError:
        save_error = 'Failed to save file.'
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
    print("Copying ", target, "to", copy_name)
    shutil.copy(workspace_path(target), workspace_path(copy_name))
    return redirect('/app/Workspace/')


def download_file(request, target):
    file_path = workspace_path(target)
    f = open(file_path, "rb")
    response = HttpResponse(f, content_type="application/x-sqlite")  # TODO: generic content type
    response['Content-Disposition'] = 'attachment; filename="' + target
    return response


def new_scenario(request):
    reset_db('scenario_db')
    reset_db('default')
    update_db_version()
    return redirect('/setup/Scenario/1/')


def prepare_supplemental_output_directory():
    """Creates a directory with the same name as the Scenario and directs the Simulation to store supplemental files in the new directory"""
    output_dir = workspace_path(scenario_filename())  # this does not have the .sqlite3 suffix
    output_args = ['--output-dir', output_dir]  # to be returned and passed to adsm.exe
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    return output_args


def adsm_executable_command():
    executables = {"Windows": 'adsm.exe', "Linux": 'adsm', "Darwin": 'adsm'}
    system_executable = os.path.join(settings.BASE_DIR, executables[platform.system()])  #TODO: KeyError
    database_file = os.path.basename(settings.DATABASES['scenario_db']['NAME'])
    output_args = prepare_supplemental_output_directory()
    return [system_executable, database_file] + output_args
