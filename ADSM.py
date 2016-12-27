import os
import sys
import multiprocessing


# TODO: Search for any and all .exe references in the whole program
print("Setting up Python...")

if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(sys.executable)
    os.environ["PATH"] += os.pathsep + os.path.join(BASE_DIR, 'bin')
    os.environ["PATH"] += os.pathsep + os.path.join(BASE_DIR, 'bin', 'env')
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
print('Running in:', BASE_DIR)

sys.path.append(BASE_DIR)
sys.path.append(os.path.join(BASE_DIR, 'bin'))
sys.path.append(os.path.join(BASE_DIR, 'bin', 'env'))

os.chdir(BASE_DIR)

multiprocessing.freeze_support()

# ----------BEGIN MAIN PROGRAM----------
import subprocess
import argparse
import threading
import _thread
import psutil
from django.utils.timezone import now


def launch_viewer():
    print("\nLaunching browser...")
    if not os.path.exists(os.path.join(settings.WORKSPACE_PATH, 'settings', 'Viewer', settings.OS_DIR)):
        os.makedirs(os.path.join(settings.WORKSPACE_PATH, 'settings', 'Viewer', settings.OS_DIR), exist_ok=True)
    log_path = os.path.join(settings.WORKSPACE_PATH, 'settings', 'Viewer', settings.OS_DIR, 'debug.log')
    console_log_path = os.path.join(settings.WORKSPACE_PATH, 'settings', 'Viewer', settings.OS_DIR, 'console.log')
    try:
        viewer_status = subprocess.call('"'+os.path.join(BASE_DIR, 'Viewer', settings.OS_DIR, 'ADSM_Beta_Viewer%s" --log-file="%s" --console-log-path="%s" --no-sandbox' % (settings.EXTENSION, log_path, console_log_path)), shell=True)
        if viewer_status != 0 and viewer_status != 9:  # The 9 is to ignore X Window System error BadDrawable when closing. TODO: Debug viewer
            raise RuntimeError("Error launching Viewer!")
    except:
        print("\nIt appears that the Viewer Application is either missing or not compatible with this system!\nYou can open a browser and navigate to http://127.0.0.1:8000")
        print("\nPress any key to close the application...")
        input()
    print("\nClosing application!")
    _thread.interrupt_main()

parser = argparse.ArgumentParser(prog='ADSM-Beta.exe')
# TODO: Tests don't run currently as the test runner won't find compiled tests.
parser.add_argument('-t', '--test', dest='test', help='run the test suite', action='store_true')
parser.add_argument('-n', '--update_name', dest='update_name', help='Query for the name of this program as known to the update server', action='store_true')
parser.add_argument('-v', '--version', dest='version', help='Get current version of program.', action='store_true')
args = parser.parse_args()

# Respond to an updater query
if args.update_name:
    print("ADSM_Beta")
    sys.exit(0)
elif args.version:
    from ADSM import __version__
    print(__version__)
    sys.exit(0)

# Check that another instance of the program isn't running
for proc in psutil.process_iter():
    try:
        proc_name = proc.name().lower()
    except psutil.AccessDenied as e:
        continue
    if 'ADSM Viewer'.lower() in proc_name:
        print("\nThere is already an instance of ADSM running!")
        print("\nPress any key to exit...")
        input()
        sys.exit(1)

print("\nPreparing Django environment...")

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ADSM.settings")

import django
django.setup()
from django.conf import settings
from django.core import management


if not os.access(settings.WORKSPACE_PATH, os.W_OK | os.X_OK) or not os.access(settings.DB_BASE_DIR, os.W_OK | os.X_OK):
    print("Your user does not have proper file permissions in the ADSM Workspace Directory!\nPlease re-run ADSM with administrative privileges.")
    print("\nPress any key to exit...")
    input()
    sys.exit(1)

if not settings.DEBUG:
    print("\nADSM is now running in the ADSM_Viewer.\nPlease do not close this window while ADSM is running.")

    if not os.path.exists(os.path.join(settings.WORKSPACE_PATH, 'settings', 'logs')):
        os.makedirs(os.path.join(settings.WORKSPACE_PATH, 'settings', 'logs'))
    output_log = os.path.join(settings.WORKSPACE_PATH, 'settings', 'logs', 'output.log')
    error_log = os.path.join(settings.WORKSPACE_PATH, 'settings', 'logs', 'error.log')

    if os.path.isfile(output_log) and os.stat(output_log).st_size > 10000000:
        os.remove(output_log)
    if os.path.isfile(error_log) and os.stat(error_log).st_size > 10000000:
        os.remove(error_log)

    with open(output_log, 'a') as log:
        log.write("STARTING AT: %s" % now())
        log.close()
    with open(error_log, 'a') as log:
        log.write("STARTING AT: %s" % now())
        log.close()

    sys.stdout = open(output_log, 'a')
    sys.sterr = open(error_log, 'a')

if args.test:
    print("\nRunning tests...")
    management.call_command('test')
else:
    # NOTE: Normally you would need to check for updates. However, graceful startup is doing this for us.

    browser = threading.Timer(1, launch_viewer)
    browser.start()

    print("\nLaunching server...")
    try:
        server_status = management.call_command('runproductionserver', port=8000, app_port=8001, silent=True)
        if server_status != 0:
            raise RuntimeError("Error launching Django Production Server!")
    except:
        if browser.is_alive():
            print("It appears that the Django Production Server Application is either missing or not compatible with this system!\nWe will launch using the debug server instead.\nMake sure your settings are set to development settings and debug=True.\n")
            management.call_command('runserver', addrport="127.0.0.1:8000", use_reloader=False)
    # management.call_command('runserver', use_reloader=False)
