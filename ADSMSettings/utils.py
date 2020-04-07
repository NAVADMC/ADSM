from itertools import chain
import os
import shutil
import re
from glob import glob
import platform
from collections import defaultdict

from django.db import OperationalError
from django.core.management import call_command
from django.db import connections, close_old_connections
from django.conf import settings
import sys
import subprocess

from ADSMSettings.models import SmSession


if os.name == "nt":
    try:
        import ctypes.wintypes
    except:
        pass  # We are already handling the exception case below


def db_path(name='scenario_db'):
    return settings.DATABASES[name]['NAME']


def workspace_path(target=None):
    path = settings.WORKSPACE_PATH

    if target is None:
        return path
    elif '/' in target or '\\' in target:
        parts = re.split(r'[/\\]+', target)  # the slashes here are coming in from URL so they probably don't match os.path.split()
        path = os.path.join(path, *parts)
        return path
    else:
        path = os.path.join(path, target)
        return path  # TODO: shlex.quote(path) if you want security


def db_list():
    dbs = []
    for root, dirs, files in os.walk(workspace_path()):
        for dir in dirs:
            if dir not in ['Example Database Queries', 'Example R Code', 'settings']:
                dir_files = os.listdir(os.path.join(workspace_path(), dir))
                for file in dir_files:
                    if file.endswith('.db') and file.replace('.db', '') != scenario_filename():
                        dbs.append((file, os.path.getmtime(os.path.join(workspace_path(), dir, file))))  # Append tuple (filename, datemodified)
                        break  # Don't add a directory more than once
        break  # only look at the top level for folders that may contain DBs
    dbs = sorted(dbs, key=lambda x: x[1], reverse=True)  # Sort by provided date
    dbs = [x[0] for x in dbs]  # Remove dates and leave just names
    return dbs


def file_list(extensions=[]):
    if isinstance(extensions, str):
        extensions = [extensions]  # container around a string
    files = [glob(workspace_path("*" + ext)) for ext in extensions]
    db_files = sorted(chain(*files), key=lambda s: s.lower())  # alphabetical, no case
    return map(lambda f: os.path.basename(f), db_files)  # remove directory and extension


def handle_file_upload(request, field_name='file', is_temp_file=False, overwrite_ok=False):
    """Writes an uploaded file into the project workspace and returns the full path to the file."""
    uploaded_file = request.FILES[field_name]
    prefix = ''
    if is_temp_file:
        prefix = 'temp/'
    if os.path.splitext(uploaded_file._name)[1].lower() in ['.db', '.sqlite', '.sqlite3']:
        if not is_temp_file:
            prefix = os.path.splitext(uploaded_file._name)[0]
        uploaded_file._name = os.path.splitext(uploaded_file._name)[0] + '.db'
    os.makedirs(workspace_path(prefix), exist_ok=True)
    file_path = workspace_path(prefix + uploaded_file._name)
    if os.path.exists(file_path) and not (is_temp_file or overwrite_ok):
        raise FileExistsError("File with the same name is already in the workspace folder. Please rename or delete the old file.")
    else:
        with open(file_path, 'wb+') as destination:
            for chunk in uploaded_file.chunks():
                destination.write(chunk)
    return file_path


def prepare_supplemental_output_directory():
    """Creates a directory with the same name as the Scenario and directs the Simulation to store supplemental files in the new directory"""
    output_dir = workspace_path('%s/%s' % (scenario_filename(), "Supplemental Output Files"))  # this does not have the .db suffix
    output_args = ['--output-dir', output_dir]  # to be returned and passed to adsm_simulation.exe
    if not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)
    return output_args


def adsm_executable_command():
    executables = {"Windows": 'adsm_simulation.exe', "Linux": 'adsm_simulation', "Darwin": 'adsm_simulation'}
    executables = defaultdict(lambda: 'adsm_simulation', executables)
    system_executable = os.path.join(settings.BASE_DIR, 'bin', executables[platform.system()])
    output_args = prepare_supplemental_output_directory()
    ret = [system_executable, db_path('scenario_db')] + output_args
    return ret


def check_for_updates():
    print("Checking for updates...")
    clear_update_flag()
    check_simulation_version()
    version = check_update()
    if version and version != 'False' and version != '0':
        print("New version available:", version)
    else:
        print("No updates currently.")
    return version


def copy_db_template(template, destination):
    try:
        close_old_connections()
        print("Copying %s database to %s..." % (template, destination))
        source = os.path.join(settings.BASE_DIR, 'Database Templates', template)
        shutil.copy(source, destination)
    except:
        print("Copying database failed!")
        raise


def copy_blank_to_session():
    try:  # just copy blank then update version
        copy_db_template('blank.db', os.path.join(settings.DB_BASE_DIR, 'activeSession.db'))
        SmSession.objects.all().update(unsaved_changes=True)
    except BaseException as err:
        print("Copying from blank scenario template failed!\nResetting database.")
        print(err)
        reset_db('scenario_db')


def copy_blank_to_settings():
    try:
        copy_db_template('settings.db', os.path.join(settings.DB_BASE_DIR, 'settings.db'))
    except BaseException as e:
        print("Copying from blank settings template failed!\nResetting database.")
        print(e)
        reset_db('default')


def graceful_startup():
    """Checks something inside of each of the database files to see if it's valid.  If not, rebuild the database."""
    print("Setting up application...")

    if not os.path.exists(workspace_path()):
        print("Creating User Directory...")
        os.makedirs(os.path.dirname(workspace_path()), exist_ok=True)
    if not os.path.exists(settings.DB_BASE_DIR):
        print("Creating DB Directory...")
        os.makedirs(settings.DB_BASE_DIR, exist_ok=True)

    print("Copying Sample Scenarios and Example Queries and Code...")
    samples_dir = os.path.join(settings.BASE_DIR, "Sample Scenarios")
    blacklisted_dirs = ["Supplemental Output Files", "Combined Outputs", "Map"]
    blacklisted_files = ["population_map.png", "population_thumbnail.png"]
    for dirpath, dirnames, files in os.walk(samples_dir):
        [os.makedirs(workspace_path(sub), exist_ok=True) for sub in dirnames if sub not in blacklisted_dirs]
        subdir = str(dirpath).replace(samples_dir, '')
        if subdir.startswith(os.path.sep):
            subdir = subdir.replace(os.path.sep, '', 1)
        if subdir.strip():
            if not os.path.exists(os.path.join(workspace_path(), subdir)):
                os.makedirs(os.path.join(workspace_path(), subdir), exist_ok=True)
        for file in files:
            if file not in blacklisted_files:
                try:
                    shutil.copy(os.path.join(dirpath, file), os.path.join(workspace_path(), subdir, file))
                except Exception as e:
                    print(e)

    print("Migrating all .sqlite3 files to .db...")
    connections.close_all()
    close_old_connections()
    for dirpath, dirnames, files in os.walk(workspace_path()):
        for file in files:
            if os.path.splitext(file)[1].lower() in ['.sqlite', '.sqlite3']:
                file_path = os.path.join(dirpath, file)
                new_file_path = os.path.splitext(file_path)[0] + '.db'
                shutil.copy(file_path, new_file_path)
                os.remove(file_path)

    print("Moving all DBs to their own folders...")
    for dirpath, dirnames, files in os.walk(workspace_path()):
        for file in files:
            if os.path.splitext(file)[1].lower() in ['.db', '.sqlite', '.sqlite3']:
                file_path = os.path.join(dirpath, file)
                new_file_path = os.path.join(dirpath, os.path.splitext(file)[0], file)
                os.makedirs(os.path.join(dirpath, os.path.splitext(file)[0]), exist_ok=True)
                shutil.copy(file_path, new_file_path)
                os.remove(file_path)
        break  # only walk over top level folder where DB files used to be saved

    print("Checking database state...")
    if not os.path.isfile(os.path.join(settings.DB_BASE_DIR, 'settings.db')) or os.stat(os.path.join(settings.DB_BASE_DIR, 'settings.db')).st_size < 10000:
        copy_blank_to_settings()
    try:
        x = SmSession.objects.get().scenario_filename  # this should be in the initial migration
        print(x)
    except OperationalError:
        reset_db('default')

    if not os.path.isfile(os.path.join(settings.DB_BASE_DIR, 'activeSession.db')) or os.stat(os.path.join(settings.DB_BASE_DIR, 'activeSession.db')).st_size < 10000:
        copy_blank_to_session()
    try:
        from ScenarioCreator.models import ZoneEffect
        ZoneEffect.objects.count()  # this should be in the initial migration
    except OperationalError:
        reset_db('scenario_db')

    update_db_version()
    SmSession.objects.all().update(simulation_crashed=False, crash_text=None)

    if getattr(sys, 'frozen', False):
        check_for_updates()
    else:
        print("Skipping update check.")
        clear_update_flag()

    print("Done setting up application.")


def reset_db(name, fail_ok=True):
    """Resets the database to a healthy state by any means necessary.  Tries to delete the file, or flush all tables, then runs the migrations from scratch.
     It now checks if the file exists.  This will throw a PermissionError if the user has the DB open in another program."""
    print("Deleting", db_path(name))
    close_old_connections()
    delete_failed = False
    if os.path.exists(db_path(name)):  # your database is corrupted and must be destroyed
        connections[name].close()
        try:
            # or you could http://stackoverflow.com/a/24501130/2291495
            os.remove(db_path(name))
        except PermissionError as err:  # must still be holding onto the file lock, clear out contents instead
            if not fail_ok:
                raise err
            else:  # I already tried manage.py flush.  It doesn't do enough
                execute = connections[name].cursor().execute
                # raw_sql = "select 'drop table ' || name || ';' from sqlite_master where type = 'table';"
                execute("PRAGMA writable_schema = 1;")
                execute("delete from sqlite_master where type in ('table', 'index', 'trigger');")
                execute("PRAGMA writable_schema = 0;")
                execute("VACUUM;")
                execute("PRAGMA INTEGRITY_CHECK;")
                print("===Dropping all Tables===")
    else:
        print(db_path(name), "does not exist")
    #creates a new blank file by migrate
    call_command('migrate', database=name, interactive=False, fake_initial=True)
    if name == 'default':  # create super user
        create_super_user()


def create_super_user():
    from django.contrib.auth.models import User
    u = User(username='ADSM', is_superuser=True, is_staff=True)
    u.set_password('ADSM')
    u.save()
    return u


def update_db_version():
    """It is critical to call migrate only with a database specified in order for the django_migration history
    to stay current with activeSession."""
    print("Checking Database states...")
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ADSM.settings")
    try:
        call_command('migrate', database='scenario_db', interactive=False, fake_initial=True)
        call_command('migrate', database='default', interactive=False, fake_initial=True)
    except:
        print("Error: Migration failed.")
    print('Done migrating databases.')


def supplemental_folder_has_contents(subfolder=''):
    """Doesn't currently include Map subdirectory.  Instead it checks for the map zip file.  TODO: This could be a page load slow down given that
    we're checking the file system every page."""
    return len(list(chain(*[glob(workspace_path(scenario_filename() + "/" + "Supplemental Output Files" + "/" + subfolder + "/*." + ext)) for ext in ['csv', 'shp', 'shx', 'dbf', 'zip']]))) > 0


def scenario_filename(new_value=None, check_duplicates=False):
    session = SmSession.objects.get()  # This keeps track of the state for all views and is used by basic_context
    if new_value:
        new_value = new_value.replace('.db', '')
        if re.search(r'[^\w\d\- \\/_\(\)\.,]', new_value):  # negative set, list of allowed characters
            raise ValueError("Special characters are not allowed: " + new_value)
        if check_duplicates:
            counter = 1
            while os.path.exists(workspace_path(new_value)):
                if counter == 1:
                    new_value = new_value + " (" + str(counter) + ")"
                else:
                    new_value = new_value[:-4] + " (" + str(counter) + ")"
                counter += 1

        session.scenario_filename = new_value
        session.save()
    return session.scenario_filename


def launch_external_program_and_exit(launch, code=0, close_self=True, cmd_args=None, launch_args=None):
    if not launch_args:
        launch_args = {}
    if not cmd_args:
        cmd_args = []
    launch = [launch, ]
    if cmd_args:
        for cmd_arg in cmd_args:
            launch.append(cmd_arg)
    launch = ' '.join(launch)
    if sys.platform == 'win32':  # Yes, this is also x64.
        CREATE_NEW_PROCESS_GROUP = 0x00000200
        DETACHED_PROCESS = 0x00000008
        launch_args.update(creationflags=DETACHED_PROCESS | CREATE_NEW_PROCESS_GROUP)
    else:
        launch_args.update(preexec_fn=os.setsid)
        launch_args.update(start_new_session=True)
    subprocess.Popen(launch, stdin=subprocess.PIPE, shell=(platform.system() != 'Darwin'), stdout=subprocess.PIPE, stderr=subprocess.PIPE, **launch_args)
    if close_self:
        sys.exit(code)


def check_simulation_version():
    """Will return None if the database is not usable"""
    close_old_connections()
    version = None
    try:
        executable = adsm_executable_command()[0]
        process = subprocess.Popen([executable, "--version --silent"], shell=(platform.system() != 'Darwin'), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            output, error = process.communicate(timeout=200)
            exit_code = process.returncode
        except:
            exit_code = 1
            output = None
        try:
            process.kill()
        except:
            pass

        if exit_code == 0:
            version = output.splitlines()[-1].decode()
    except:
        print("Unable to get Simulation Version!")
        return None
    try:
        SmSession.objects.all().update(simulation_version=version)
    except:
        print("Unable to store Simulation Version!")

    return version


def npu_update_info():
    new_version = None
    try:
        npu = os.path.join(settings.BASE_DIR, 'npu'+settings.EXTENSION)
        process = subprocess.Popen([npu, "--check_update", "--silent"], shell=(platform.system() != 'Darwin'), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            output, error = process.communicate(timeout=60000)
            exit_code = process.returncode
        except:
            exit_code = 1
            output = None
        try:
            process.kill()
        except:
            pass

        if output:
            new_version = output.splitlines()[-1].decode().strip()
    except:
        print("Unable to get ADSM Version!")

    return new_version


def clear_update_flag():
    try:  # database may not exist
        session = SmSession.objects.get()
        session.update_available = False
        session.save()
    except:
        print("Unable to clear Update Flags!")


def check_update():
    close_old_connections()

    version = npu_update_info()
    try:
        SmSession.objects.all().update(update_available=version)
    except:
        print("Unable to store ADSM Version!")

    return version
