import os
import sys
import subprocess
import shutil
from time import sleep
from argparse import ArgumentParser

parser = ArgumentParser(prog='adsm_update.exe')
parser.add_argument('-p', '--path', dest='path', action='store', default=None, type=str, help="Path of ADSM installation root directory")
parser.add_argument('-z', '--finalize', dest='finalize', action='store_true', help="Indicates that this is the third invocation, where the program clear the update flags")

args = parser.parse_args()

run_now = False
if args.path:
    run_now = True
sleep(3)

DETACHED_PROCESS = 0x00000008


def import_django(BASE_DIR):
    sys.path.append(os.path.join(BASE_DIR, 'src'))

    # Discretely import django items
    os.chdir(os.path.join(BASE_DIR, 'src'))
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ADSM.settings")
    exec("import django")
    exec("django.setup()")


def import_dependencies(venv=True, django=True):
    print("Importing Python dependencies and setting local path...")
    if getattr(sys, 'frozen', False):
        BASE_DIR = os.path.dirname(os.path.dirname(sys.executable))
        os.environ["PATH"] += os.pathsep + os.path.join(BASE_DIR, 'bin')  # Path to the library.zip file
    else:
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    print(BASE_DIR)

    sys.path.append(BASE_DIR)
    if venv:
        sys.path.append(os.path.join(BASE_DIR, "DLLs"))
        sys.path.append(os.path.join(BASE_DIR, "Lib"))
        sys.path.append(os.path.join(BASE_DIR, "Lib", "plat-win"))
        sys.path.append(os.path.join(BASE_DIR, "Lib", "lib-tk"))
        sys.path.append(os.path.join(BASE_DIR, "bin"))
        sys.path.append(os.path.join(BASE_DIR, "Scripts"))
        sys.path.append(os.path.join(BASE_DIR, "Lib", "site-packages"))
        path_all_the_eggs(BASE_DIR)

        if django:
            import_django(BASE_DIR)

    os.chdir(BASE_DIR)
    return BASE_DIR


def path_all_the_eggs(BASE_DIR):
    packages = os.path.join(BASE_DIR, "Lib", "site-packages")
    for folder in os.listdir(packages):
        subfolder = os.path.join(packages, folder)
        if os.path.isdir(subfolder):
            if folder[-4:] == '.egg':
                sys.path.append(subfolder)


def quote_path_for_system_call(path):
    if not path.startswith('"'):
        path = '"' + path
    if not path.endswith('"'):
        path += '" '  # Keep the trailing space here to help with concatenation later on!
    return path


def forceful_git_cleanup(BASE_DIR):
    try:
        import psutil
        print("Kill all git processes")
        for process in psutil.process_iter():
            try:
                if 'git' in process.name():
                    process.kill()
                    # make sure it's dead
            except (psutil.AccessDenied, PermissionError) as e:
                pass  # print("IMPORTANT: Run this program again as administrator if this doesn't work.", e)
    except ImportError:
        pass
    
    lock_file = os.path.join(BASE_DIR, ".git", "index.lock")
    if os.path.exists(lock_file):
        try:
            os.remove(lock_file)
        except:
            print("IMPORTANT: You will need to manually delete ", lock_file, "before ADSM can update.")
            sleep(10)
            sys.exit()


if run_now:  # We are in a safe location and can call git against the passed in path to update
    BASE_DIR = import_dependencies(venv=False, django=False)

    forceful_git_cleanup(BASE_DIR)

    src_dir = os.path.join(args.path, 'src')
    sys.path.append(src_dir)
    os.chdir(src_dir)

    from git.git import reset_and_update_adsm
    reset_and_update_adsm()

    UPDATE_PROGRAM = os.path.join(args.path, 'bin', 'adsm_update.exe')
    pid = subprocess.Popen(quote_path_for_system_call(UPDATE_PROGRAM) + ' --finalize', shell=True, creationflags=DETACHED_PROCESS).pid
    sys.exit()
elif args.finalize:  # The external version of the update has called us back after performing an update
    BASE_DIR = import_dependencies()

    exec('from ADSMSettings.utils import clear_update_flag, workspace_path')

    clear_update_flag()

    update_now = workspace_path('bin/adsm_update.exe')
    os.remove(update_now)
    os.remove(workspace_path('bin/library.zip'))

    MAIN_PROGRAM = os.path.join(BASE_DIR, 'adsm.exe')
    pid = subprocess.Popen(MAIN_PROGRAM, shell=True, creationflags=DETACHED_PROCESS).pid
    sys.exit()
else:  # This is the first call into the update program, so we need to copy our self out to a safe location
    BASE_DIR = import_dependencies()

    exec('from ADSMSettings.utils import workspace_path')
    os.makedirs(workspace_path('bin'), exist_ok=True)
    update_now = workspace_path('bin/adsm_update.exe')
    shutil.copy(os.path.join(BASE_DIR, 'bin', 'adsm_update.exe'), update_now)
    shutil.copy(os.path.join(BASE_DIR, 'bin', 'library.zip'), workspace_path('bin/library.zip'))

    pid = subprocess.Popen(quote_path_for_system_call(update_now) + ' --path=' + quote_path_for_system_call(BASE_DIR), shell=True, creationflags=DETACHED_PROCESS).pid
    sys.exit()
