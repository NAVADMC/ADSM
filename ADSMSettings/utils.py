from itertools import chain
import os
import subprocess
import re
from glob import glob
import platform
from collections import defaultdict

from git.git import git
from django.db import OperationalError
from django.core.management import call_command
from django.db import connections, close_old_connections
from django.conf import settings
from ADSMSettings.models import SmSession, scenario_filename


def db_name(name='scenario_db'):
    full_path = settings.DATABASES[name]['NAME']
    return os.path.basename(full_path)


def workspace_path(target):
    if '/' in target or '\\' in target:
        parts = re.split(r'[/\\]+', target)  # the slashes here are coming in from URL so they probably don't match os.path.split()
        return os.path.join("workspace", *parts)
    return os.path.join("workspace", target)


def file_list(extension=''):
    db_files = sorted(glob("./workspace/*" + extension), key=lambda s: s.lower())  # alphabetical, no case
    return map(lambda f: os.path.basename(f), db_files)  # remove directory and extension


def handle_file_upload(request, field_name='file', is_temp_file=False):
    """Writes an uploaded file into the project workspace and returns the full path to the file."""
    uploaded_file = request.FILES[field_name]
    prefix = ''
    if is_temp_file:
        prefix = 'temp/'
        os.makedirs(workspace_path(prefix), exist_ok=True)
    filename = workspace_path(prefix + uploaded_file._name)
    with open(filename, 'wb+') as destination:
        for chunk in uploaded_file.chunks():
            destination.write(chunk)
    return filename


def prepare_supplemental_output_directory():
    """Creates a directory with the same name as the Scenario and directs the Simulation to store supplemental files in the new directory"""
    output_dir = workspace_path(scenario_filename())  # this does not have the .sqlite3 suffix
    output_args = ['--output-dir', output_dir]  # to be returned and passed to adsm_simulation.exe
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    return output_args


def adsm_executable_command():
    executables = {"Windows": 'adsm_simulation.exe', "Linux": 'adsm_simulation', "Darwin": 'adsm_simulation'}
    executables = defaultdict(lambda: 'adsm_simulation', executables)
    system_executable = os.path.join(settings.BASE_DIR, executables[platform.system()])
    database_file = os.path.basename(settings.DATABASES['scenario_db']['NAME'])
    output_args = prepare_supplemental_output_directory()
    return [system_executable, database_file] + output_args


def graceful_startup():
    """Checks something inside of each of the database files to see if it's valid.  If not, rebuild the database."""
    try:
        SmSession.objects.get().update_available
    except OperationalError:
        reset_db('default')
        
    try:
        from ScenarioCreator.models import ZoneEffect
        ZoneEffect.objects.count()
    except OperationalError:
        reset_db('scenario_db')
    
    update_db_version()
    session = SmSession.objects.get()
    session.update_on_startup = False
    session.save()


def reset_db(name, fail_ok=True):
    """ It now checks if the file exists.  This will throw a PermissionError if the user has the DB open in another program."""
    print("Deleting", db_name(name))
    close_old_connections()
    delete_failed = False
    if os.path.exists(db_name(name)):
        connections[name].close()
        try:
            os.remove(db_name(name))
        except PermissionError as err:
            if not fail_ok:
                raise err
            else: 
                delete_failed = True
    else:
        print(db_name(name), "does not exist")
    #creates a new blank file by migrate 
    call_command('migrate',
                 # verbosity=0,
                 interactive=False,
                 database=connections[name].alias)
    if name == 'default' and not delete_failed:  # create super user
        from django.contrib.auth.models import User
        u = User(username='ADSM', is_superuser=True, is_staff=True)
        u.set_password('ADSM')
        u.save()


def update_db_version():
    print("Checking Scenario version")
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ADSM.settings")
    try:
        call_command('migrate',
                     # verbosity=0,
                     interactive=False)
    except:
        print("Error: Migration failed.")
    print('Done creating database')


def update_requested():
    try:
        a_size = os.stat(connections.databases['scenario_db']['NAME']).st_size
        s_size = os.stat(connections.databases['default']['NAME']).st_size
        if a_size < 500 or s_size < 500:  # size in bytes
            return False
    except:
        return False
        
    try:
        session = SmSession.objects.get()
        if session.update_on_startup:
            return True
    except:
        pass
    finally:
        close_old_connections()

    return False


def update_is_needed():
    print("Checking for updates...")
    try:
        os.chdir(settings.BASE_DIR)

        command = git + ' rev-parse --abbrev-ref HEAD'
        current_branch = subprocess.check_output(command, shell=True).decode().strip()

        # Go ahead and fetch the current branch
        command = git + ' fetch origin ' + current_branch
        subprocess.call(command, shell=True)

        command = git + ' rev-parse FETCH_HEAD'
        fetched_sha = subprocess.check_output(command, shell=True).decode().strip()
        command = git + ' rev-parse HEAD'
        head_sha = subprocess.check_output(command, shell=True).decode().strip()

        if fetched_sha != head_sha:
            print("An update is required.")
            return True
        print("There are currently no updates.")
        return False
    except:
        print ("Failed in checking if an update is required!")
        return False


def update_adsm():
    if update_is_needed():
        print("Attempting to update files...")
        try:
            command = git + ' stash'
            subprocess.call(command, shell=True)  # trying to get rid of settings.sqlite3 change
            command = git + ' reset --hard'
            subprocess.call(command, shell=True)

            command = git + ' rebase FETCH_HEAD'
            git_status = subprocess.check_output(command, shell=True)
            # TODO: Make sure the pull actually worked

            print("Successfully updated.")
            return True
        except:
            print("Failed to update!")
            try:
                command = git + ' reset'
                subprocess.call(command, shell=True)
                print("Reset to original state.")
            except:
                print("Failed to gracefully reset to original state!")

            return False
        finally:
            try:
                session = SmSession.objects.get()
                session.update_on_startup = False
                session.update_available = False
                session.save()
            except:
                pass
            
            command = git + ' stash apply'
            subprocess.call(command, shell=True)  # TODO: What if the stash apply has a conflict?
    else:
        return True


def reset_and_update_adsm():
    try:
        print("Resetting all files to base state...")
        command = git + ' reset --hard'
        subprocess.call(command, shell=True)

        print("Attempting to update files...")
        command = git + ' rev-parse --abbrev-ref HEAD'
        current_branch = subprocess.check_output(command, shell=True).decode().strip()

        # Go ahead and fetch the current branch
        command = git + ' fetch origin ' + current_branch
        subprocess.call(command, shell=True)

        command = git + ' rebase FETCH_HEAD'
        git_status = subprocess.check_output(command, shell=True)

        print("Successfully updated.")
        return True
    except:
        print("Failed to update!")
        try:
            command = git + ' reset --hard'
            subprocess.call(command, shell=True)
        except:
            print("Failed to reset files! You are probably in a bad state.")
        return False
    finally:
        try:
            session = SmSession.objects.get()
            session.update_on_startup = False
            session.update_available = False
            session.save()
        except:
            pass


def supplemental_folder_has_contents(subfolder=''):
    """Doesn't currently include Map subdirectory.  Instead it checks for the map zip file.  TODO: This could be a page load slow down given that
    we're checking the file system every page."""
    return len(list(chain(*[glob(workspace_path(scenario_filename() + subfolder + "/*." + ext)) for ext in ['csv', 'shp', 'shx', 'dbf', 'zip']]))) > 0