import os
import sys
import subprocess
import multiprocessing
import argparse
import threading
import _thread


def launch_viewer():
    print("Launching browser...")
    subprocess.call(os.path.join(BASE_DIR, 'Viewer', 'ADSM Viewer.exe'))
    print("Closing application!")
    _thread.interrupt_main()


print("Setting up Python...")

if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(sys.executable)
    os.environ["PATH"] += os.pathsep + os.path.join(BASE_DIR, 'bin')
    os.environ["PATH"] += os.pathsep + os.path.join(BASE_DIR, 'bin', 'env')
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
print(BASE_DIR)

sys.path.append(BASE_DIR)
sys.path.append(os.path.join(BASE_DIR, 'bin'))
sys.path.append(os.path.join(BASE_DIR, 'bin', 'env'))

os.chdir(BASE_DIR)

multiprocessing.freeze_support()

parser = argparse.ArgumentParser(prog='adsm.exe')
# TODO: Tests don't run currently as the test runner won't find compiled tests.
parser.add_argument('-t', '--test', dest='test', help='run the test suite', action='store_true')
parser.add_argument('-n', '--update_name', dest='update_name', help='Query for the name of this program as known to the update server', action='store_true')
parser.add_argument('-v', '--version', dest='version', help='Get current version of program.', action='store_true')
args = parser.parse_args()


def launch_external_program_and_exit(launch, code=0, cmd_args=None, launch_args=None):
    if not launch_args:
        launch_args = {}
    if not cmd_args:
        cmd_args = []
    launch = [launch, ]
    if cmd_args:
        for cmd_arg in cmd_args:
            launch.append(cmd_arg)
    if sys.platform == 'win32':  # Yes, this is also x64.
        CREATE_NEW_PROCESS_GROUP = 0x00000200
        DETACHED_PROCESS = 0x00000008
        launch_args.update(creationflags=DETACHED_PROCESS | CREATE_NEW_PROCESS_GROUP)
    else:
        launch_args.update(preexec_fn=os.setsid)
        launch_args.update(start_new_session=True)
    subprocess.Popen(launch, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, **launch_args)
    sys.exit(code)

# Respond to an updater query
if args.update_name:
    print("ADSM")
    sys.exit(0)
elif args.version:
    from ADSM import __version__
    print(__version__)
    sys.exit(0)


print("Preparing Django environment...")

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ADSM.settings")

import django
django.setup()
from django.conf import settings
from django.core import management


def check_for_updates():
    from ADSMSettings.utils import clear_update_flag, check_simulation_version, check_update

    clear_update_flag()
    check_simulation_version()
    check_update()
    return


if args.test:
    print("Running tests...")
    management.call_command('test')
else:
    update_checker = threading.Timer(.1, check_for_updates)
    update_checker.start()

    browser = threading.Timer(1, launch_viewer)
    browser.start()

    print("Launching server...")
    management.call_command('runproductionserver', port=8000, app_port=8001)
    # management.call_command('runserver', use_reloader=False)
