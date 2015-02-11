"""
I know the order of this file is odd, but some things need to be done before all the imports happen...

Things this file should do:
1) It should be run with the python interpreter that is in the VirtualEnv that has ONLY the dependencies for this project.
2) It should copy the site_packages (or dist_packages) folder of the running python interpreter to this folder
3) It should compile the CEngine, then copy adsm.exe to the root
4) It should copy in a default state settings.sqlite3 file to the root
5) It should copy in blank.sqlite3 to activeSession.sqlite3 to the root
6) It should run the collectstatic management command
7) It should run the cx_freeze compiler with the ADSM.py file as the target
8) It should zip up all the files to be sent to other users
"""
import sys
import os


def query_yes_no(question, default='yes'):
    valid = {'yes': True, 'y': True, "no": False, 'n': False}

    if default is None:
        prompt = " [y/n] "
    elif default in ['yes', 'y']:
        prompt = " [Y/n] "
    elif default in ['no', 'n']:
        prompt = " [y/N] "
    else:
        raise ValueError("Invalid default answer!")

    while True:
        sys.stdout.write('\n' + question + prompt)

        choice = input().lower()

        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no'.\n")


print("You should only run this compile script if you are in a CLEAN VirtualEnv!\n"
      "The VirtualEnv will be deployed with the project, so make sure it ONLY has the REQUIRED dependencies installed!")
if not query_yes_no("Are you in a CLEAN Python Environment?", default='no'):
    sys.exit()

print("\nDO NOT deploy with a folder that has your Git Credentials in it!\n"
      "You MUST be running this compile script in a repo that you Checked Out as an Anonymous User with Read Only access!")
if not query_yes_no("Are you in a Repo that is Checked Out by an Anonymous User?", default='no'):
    sys.exit()

compile_c_engine = query_yes_no("\nDo you want to attempt to compile the CEngine?", default='no')

##########
# Cleanup root folder
# This is done before all other imports since we will need to clean out some pyd files that get loaded by python
##########
print("Cleaning base directory...")
BASE_DIR = os.path.dirname(os.path.realpath(__file__))

from distutils.dir_util import copy_tree, remove_tree

# Remove these folders from any previous compiles
folders_to_delete = ['build', 'Lib']
for folder in folders_to_delete:
    try:
        remove_tree(os.path.join(BASE_DIR, folder))
    except:
        pass

files_to_save = ['adsm_simulation.exe', 'libglib-2.0-0.dll', 'libiconv-2.dll', 'libintl-8.dll', 'sqlite3.exe']
for file in os.listdir(BASE_DIR):
    # Only delete these files from the top directory
    if (file.endswith(".pyd") or file.endswith(".dll") or file.endswith(".zip") or file.endswith(".exe") or file.endswith(".manifest")) and file not in files_to_save:
        os.remove(file)
for root, dirs, files in os.walk(BASE_DIR):
    for file in files:
        # Delete all these from any where
        if (file.endswith(".pyc") or file.endswith(".pyo")) and file not in files_to_save:
            os.remove(os.path.join(root, file))

# Specific files to delete in the root that aren't caught in the general case above
files_to_delete = ['activeSession.sqlite3', 'settings.sqlite3']
for file in files_to_delete:
    try:
        os.remove(os.path.join(BASE_DIR, file))
    except:
        pass

# Undelete any specific files needed
import subprocess
from git.git import git
files_to_undelete = ['Lib/.gitignore', ]
for file in files_to_undelete:
    command = git + ' checkout ' + file
    subprocess.call(command, shell=True)

# Remaining imports
import errno
import subprocess
from subprocess import CalledProcessError
import shutil

import zipfile

##########
# Gather Path info and setup environment
##########
print("Noting directory structure.")

print("Project:", BASE_DIR)
os.chdir(BASE_DIR)

PYTHON_INSTALL = getattr(sys, 'prefix', None)
PYTHON = os.path.join(PYTHON_INSTALL, 'Scripts', 'python.exe')

print("Python:", PYTHON_INSTALL)
if not PYTHON_INSTALL:
    sys.exit()

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ADSM.settings")
import django
django.setup()
from django.core import management

##########
# Copy all project dependencies into the root for deployment
# This is things like matplotlib, django, pandas...
# Currently, we are expecting that the executing environment is a clean environment only used for ADSM
# If you run this in your normal python install (not dedicated VirtualEnv), then excess dependencies will be copied
##########
print("Copying dependencies...")

try:
    copy_tree(os.path.join(PYTHON_INSTALL, 'Lib'), os.path.join(BASE_DIR, 'Lib'))
    pass
except OSError as e:
    if e.errno == errno.ENOTDIR:
        raise OSError("Unknown site_packages and/or Python Lib configuration. Found file, expected folder!")
    else:
        raise

print("Cleaning dependencies...")

for root, dirs, files in os.walk(os.path.join(BASE_DIR, 'Lib')):
    for filename in files:
        if filename.endswith(".pyc"):
            os.remove(os.path.join(root, filename))
    if root.endswith(".egg-info"):
        remove_tree(root)


##########
# Compile CEngine
##########
# Compile the CEngine (but only if required environment is correctly setup, else pull already compiled exe into root)
if compile_c_engine and os.path.isfile(os.path.join(BASE_DIR, 'CEngine', 'bootstrap')):
    print("Compiling CEngine...")
    any_compile_step_failed = False
    os.chdir(os.path.join(BASE_DIR, 'CEngine'))
    print('Running bootstrap script...', end=' ')
    try:
        subprocess.check_output(['sh', 'bootstrap'], stderr=subprocess.STDOUT)
        print('succeeded')
    except CalledProcessError as e:
        any_compile_step_failed = True
        print('failed')
        print(e.output)
    
    if not any_compile_step_failed:
        print('Running configure script...', end=' ')
        try:
            subprocess.check_output(['sh', 'configure', '--disable-debug'], stderr=subprocess.STDOUT)
            print('succeeded')
        except CalledProcessError as e:
            any_compile_step_failed = True
            print('failed')
            print(e.output)
    
    if not any_compile_step_failed:
        print('Running make...', end=' ')
        try:
            subprocess.check_output(['make'], stderr=subprocess.STDOUT)
            print('succeeded')
        except CalledProcessError as e:
            if 'dia: Command not found' in e.output:
                # This error message is OK. The Dia diagramming tool is used to
                # create images for the built-in documentation, but Dia is not
                # available in MinGW. But if "make" gets to this point, then it
                # succeeded in making the executable.
                print('succeeded')
            else:
                any_compile_step_failed = True
                print('failed')
                print(e.output)
    
    exe_name = 'adsm_simulation.exe'
    
    if any_compile_step_failed:
        print('One or more compile steps failed. Will not overwrite %s in top-level directory.' % exe_name)
    else:
        print('Copying %s to top-level directory.' % exe_name)
        shutil.copy(os.path.join(os.curdir, 'main_loop', exe_name), BASE_DIR)
    os.chdir(BASE_DIR)

##########
# Compile the Python Entry Point and Python Executable
# Then zip everything up into an archive for sending away
##########
print("Compiling ADSM.py and Python into executable...")

SETUP_FILE = os.path.join(BASE_DIR, 'setup.py')
subprocess.call(PYTHON + ' ' + SETUP_FILE + ' build_exe', shell=True)

##########
# Prepare project root
# Collect static
# Zip up all the files
##########
print("Preparing project root for deployment")

management.call_command('collectstatic', interactive=False, clear=True)
print("\n")
copy_tree(os.path.join(BASE_DIR, 'build', 'exe.win-amd64-3.4'), BASE_DIR)

# Checkout old versions of files that probably didn't change (mostly update executables)
files_to_reset = ['adsm_update.exe', 'adsm_force_reset_and_update.exe']
from git.git import git
for file in files_to_reset:
    command = git + ' checkout ' + file
    subprocess.call(command, shell=True)

print("Please move to another terminal (or PyCharm) and run the Test Suite now before committing.")
if not query_yes_no("Were the Test Suite results acceptable?", default='yes'):
    sys.exit()

# Now do a compile commit to the repo.
# You need to do the commit before zipping up the deployable or the zip will be a commit behind.
if query_yes_no("Would you like to commit this compile?", default='no'):
    command = git + ' add -u'
    subprocess.call(command, shell=True)
    command = git + ' status'
    subprocess.call(command, shell=True)

    print("Look above and check if the commit is staged correctly.\n"
          "If you need to make changes, please do so now in another terminal then come back here when ready.")
    if not query_yes_no("Are you ready to commit?", default='no'):
        command = git + ' reset'
        subprocess.call(command, shell=True)
        sys.exit()
    else:
        from datetime import datetime
        timestamp = datetime.now().strftime('%m/%d/%Y @ %H:%M')
        command = git + ' commit -m "Windows Staging Compile ' + timestamp + '"'
        subprocess.call(command, shell=True)
        command = git + ' push'
        subprocess.call(command, shell=True)

if query_yes_no("Would you like to zip up the deployable?", default='no'):
    # TODO: Fix zipping files as it doesn't work yet.
    print("Zipping output into deployable...")
    deployable_path = os.path.join(BASE_DIR, 'ADSM_Distributable.zip')
    if os.path.exists(deployable_path):
        os.remove(deployable_path)

    deployable_path_len = len(os.path.dirname(deployable_path).rstrip(os.sep)) + 1

    folders_to_ignore = ['build', '.idea', 'cef', 'CEngine', 'development_scripts']
    folders_to_ignore = [os.path.join(BASE_DIR, x) for x in folders_to_ignore]

    files_to_ignore = ['ADSM_Distributable.zip', ]

    with zipfile.ZipFile(deployable_path, mode='w', compression=zipfile.ZIP_DEFLATED) as deployable:
        for root, dirs, files in os.walk(BASE_DIR):
            if root in folders_to_ignore:
                continue
            else:
                for filename in files:
                    if filename in files_to_ignore:
                        continue
                    else:
                        path = os.path.join(root, filename)
                        entry = path[deployable_path_len:]
                        deployable.write(os.path.join('ADSM', path), entry)

print("Done.")
