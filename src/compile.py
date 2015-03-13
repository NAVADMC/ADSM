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
      "You MUST be running this compile script in a repo that you Checked Out as an Anonymous User (https) with Read Only access!\n"
      "You should also only run the compile script in a repo that has only a single branch checked out.")
if not query_yes_no("Are you in a Repo that Single Branch Checked Out by an Anonymous User?", default='no'):
    sys.exit()

##########
# Cleanup root folder
# This is done before all other imports since we will need to clean out some pyd files that get loaded by python
##########
print("Cleaning base directory...")
BASE_DIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

os.chdir(BASE_DIR)

from distutils.dir_util import copy_tree, remove_tree

# Remove these folders from any previous compiles
folders_to_delete = ['build', 'Lib', os.path.join('src', 'nginx')]
for folder in folders_to_delete:
    try:
        remove_tree(os.path.join(BASE_DIR, folder))
    except:
        pass

files_to_save = ['adsm_simulation.exe', 'libglib-2.0-0.dll', 'libiconv-2.dll', 'libintl-8.dll', 'sqlite3.exe', 'msvcp100.dll', 'libsqlite3-0.dll']
for file in os.listdir(os.path.join(BASE_DIR, "bin")):
    # Only delete these files from the top directory
    if (file.endswith(".pyd") or file.endswith(".dll") or file.endswith(".zip") or file.endswith(".exe") or file.endswith(".manifest") or file.endswith(".log")) and file not in files_to_save:
        os.remove(os.path.join(BASE_DIR, 'bin', file))
for root, dirs, files in os.walk(BASE_DIR):
    for file in files:
        # Delete all these from any where
        if (file.endswith(".pyc") or file.endswith(".pyo") or file.endswith(".log")):
            os.remove(os.path.join(root, file))

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
PYTHON_INSTALL = getattr(sys, 'prefix', None)
PYTHON = os.path.join(PYTHON_INSTALL, 'Scripts', 'python.exe')

print("Python:", PYTHON_INSTALL)
if not PYTHON_INSTALL:
    sys.exit()

os.chdir(os.path.join(BASE_DIR, "src"))

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
# Compile the Python Entry Point and Python Executable
# Then zip everything up into an archive for sending away
##########
print("Compiling ADSM.py and Python into executable...")

os.chdir(BASE_DIR)

SETUP_FILE = os.path.join(BASE_DIR, 'setup.py')
subprocess.call(PYTHON + ' ' + SETUP_FILE + ' build_exe', shell=True)

##########
# Prepare project root
# Collect static
# Zip up all the files
##########
print("Preparing project root for deployment")

os.chdir(os.path.join(BASE_DIR, 'src'))

management.call_command('collectstatic', interactive=False, clear=True)
print("\n")

os.chdir(BASE_DIR)

copy_tree(os.path.join(BASE_DIR, 'build', 'exe.win-amd64-3.4'), os.path.join(BASE_DIR, 'bin'))
shutil.move(os.path.join(BASE_DIR, 'bin', 'ADSM.exe'), os.path.join(BASE_DIR, 'ADSM.exe'))
shutil.copy(os.path.join(BASE_DIR, 'bin', 'library.zip'), os.path.join(BASE_DIR, 'library.zip'))
shutil.copy(os.path.join(BASE_DIR, 'bin', 'MSVCR100.dll'), os.path.join(BASE_DIR, 'MSVCR100.dll'))
shutil.copy(os.path.join(BASE_DIR, 'bin', 'python34.dll'), os.path.join(BASE_DIR, 'python34.dll'))

remove_tree(os.path.join(BASE_DIR, 'build'))

library_update_required = 3
if not query_yes_no("Did adsm_update.exe change?", default='no'):
    library_update_required -= 1
    # Checkout old versions of files that probably didn't change (mostly update executables)
    files_to_reset = [os.path.join(BASE_DIR, 'bin', 'adsm_update.exe'), ]
    from git.git import git
    for file in files_to_reset:
        command = git + ' checkout ' + file
        subprocess.call(command, shell=True)

if not query_yes_no("Did adsm_force_reset_and_update.exe change?", default='no'):
    library_update_required -= 1
    # Checkout old versions of files that probably didn't change (mostly update executables)
    files_to_reset = [os.path.join(BASE_DIR, 'bin', 'adsm_force_reset_and_update.exe'), ]
    from git.git import git
    for file in files_to_reset:
        command = git + ' checkout ' + file
        subprocess.call(command, shell=True)

if not query_yes_no("Did the ADSM.exe change?", default='no'):
    library_update_required -= 1
    # Checkout old versions of files that probably didn't change (mostly update executables)
    files_to_reset = [os.path.join(BASE_DIR, 'adsm.exe'),]
    from git.git import git
    for file in files_to_reset:
        command = git + ' checkout ' + file
        subprocess.call(command, shell=True)

if not library_update_required:
    # Checkout old versions of files that probably didn't change (mostly update executables)
    files_to_reset = [os.path.join(BASE_DIR, 'bin', 'library.zip'), os.path.join(BASE_DIR, 'library.zip')]
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

    # Figure out the name of the zip file
    sys.stdout.write('\nWhat is the ADSM Simulation Version (3.2.22)? ')
    sim_version = input()
    sys.stdout.write('\nWhat is the ADSM Viewer Version (RC4.1)? ')
    viewer_version = input()

    deployable_path = os.path.join(BASE_DIR, 'ADSM_' + str(sim_version) + '-' + str(viewer_version) + '.zip')
    if os.path.exists(deployable_path):
        os.remove(deployable_path)

    deployable_path_len = len(os.path.dirname(deployable_path).rstrip(os.sep)) + 1

    folders_to_ignore = ['build', '.idea', ]
    folders_to_ignore = [os.path.join(BASE_DIR, x) for x in folders_to_ignore]

    files_to_ignore = [os.path.basename(deployable_path), ]

    with zipfile.ZipFile(deployable_path, mode='w', compression=zipfile.ZIP_DEFLATED) as deployable:
        for root, dirs, files in os.walk(BASE_DIR):
            if not any([ignored in root for ignored in folders_to_ignore]):
                for filename in files:
                    if filename not in files_to_ignore:
                        path = os.path.join(root, filename)
                        entry = path[deployable_path_len:]
                        deployable.write(os.path.join('ADSM', path), entry)

print("Done.")
