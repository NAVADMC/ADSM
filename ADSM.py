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
import json
import threading
import _thread
import psutil
import socket

from tkinter import Tk
from tkinter.filedialog import askdirectory
from tkinter.messagebox import askyesno, Message

from django.utils.timezone import now


def launch_viewer(server_port):
    print("\nLaunching browser...")
    if not os.path.exists(os.path.join(settings.WORKSPACE_PATH, 'settings', 'Viewer', settings.OS_DIR)):
        os.makedirs(os.path.join(settings.WORKSPACE_PATH, 'settings', 'Viewer', settings.OS_DIR), exist_ok=True)
    log_path = os.path.join(settings.WORKSPACE_PATH, 'settings', 'Viewer', settings.OS_DIR, 'debug.log')
    # console_log_path = os.path.join(settings.WORKSPACE_PATH, 'settings', 'Viewer', settings.OS_DIR, 'console.log')  # The new viewer created 11/26/2019 doesn't create separate browser and javascript logs. Everything goes into log_path above.
    try:
        # viewer_status = subprocess.call('"'+os.path.join(BASE_DIR, 'Viewer', settings.OS_DIR, 'ADSM_Beta_Viewer%s" --log-file="%s" --console-log-path="%s" --url="%s" --no-sandbox' % (settings.EXTENSION, log_path, console_log_path, "http://127.0.0.1:%s" % server_port)), shell=True)
        viewer_status = subprocess.call('"'+os.path.join(BASE_DIR, 'Viewer', settings.OS_DIR, 'ADSM_Beta_Viewer%s" "%s" "%s" "%s" "%s"' % (settings.EXTENSION, "http://127.0.0.1:%s" % server_port, "ADSM Beta Viewer", log_path, os.path.join(settings.BASE_DIR, 'bin', 'env', 'favicon.ico'))), shell=True)
        if viewer_status != 0 and viewer_status != 9:  # The 9 is to ignore X Window System error BadDrawable when closing. TODO: Debug viewer
            raise RuntimeError("Error launching Viewer!")
    except:
        print("\nIt appears that the Viewer Application is either missing or not compatible with this system!\nYou can open a browser and navigate to http://127.0.0.1:%s" % server_port)
        print("\nPress any key to close the application (unless manually viewing in the browser)...")
        input()
    print("\nClosing application!")
    _thread.interrupt_main()


def find_available_ports():
    print("Looking for available ports...")
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('', 0))
    app_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    app_socket.bind(('', 0))

    server_port = server_socket.getsockname()[1]
    app_port = app_socket.getsockname()[1]

    server_socket.close()
    app_socket.close()

    print("Found ports %s and %s." % (server_port, app_port))

    # NOTE: We now have the chance for a race condition.
    # Since we closed the sockets above so the caller can now bind to the ports we found,
    # another program can possibly come in and bind the ports before our program can rebind.
    return server_port, app_port


parser = argparse.ArgumentParser(prog='ADSM-Beta.exe')
# TODO: Tests don't run currently as the test runner won't find compiled tests.
parser.add_argument('-t', '--test', dest='test', help='run the test suite', action='store_true')
parser.add_argument('-n', '--update_name', dest='update_name', help='Query for the name of this program as known to the update server', action='store_true')
parser.add_argument('-v', '--version', dest='version', help='Get current version of program.', action='store_true')

# arguments for auto
parser.add_argument('--run-all-scenarios', dest='run_all_scenarios',
                    help='Run all Scenarios in the Workspace with the ADSM Auto Scenario Runner unless a file called DO.NOT.RUN is present in the scenario folder.', action='store_true')
parser.add_argument('--exclude-scenarios', dest='exclude_scenarios',
                    help='A list of scenarios to exclude from the ADSM Auto Scenario Runner. Ex: "Scenario 1" "Scenario 2"', nargs='+')
parser.add_argument('--exclude-scenarios-list', dest='exclude_scenarios_list',
                    help="File that contains a list of scenario names to exclude from the ADSM Auto Scenario Runner, one per line.", action='store')
parser.add_argument('--run-scenarios', dest='run_scenarios',
                    help='A list of scenarios for the ADSM Auto Scenario Runner to run. Ex: "Scenario 1" "Scenario 2"', nargs="+")
parser.add_argument('--run-scenarios-list', dest='run_scenarios_list',
                    help='File that contains a list of scenario scenario names to run with the ADSM Auto Scenario Runner, one per line.', action='store')
parser.add_argument('--workspace-path', dest='workspace_path',
                    help="Give a different workspace path to pull scenarios from for the ADSM Auto Scenario Runner.", action='store')
parser.add_argument('--output-path', dest='output_path',
                    help="Where the ADSM Auto Scenario Runner should store output logs.", action='store')
parser.add_argument('--max-iterations', dest='max_iterations',
                    help="Maximum number of iterations any single simulation can run with the ADSM Auto Scenario Runner.", action='store')

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

print("\nPreparing Workspace...")
if os.path.exists(os.path.join(BASE_DIR, 'workspace')):
    # Rename any old 'workspace' folders to 'ADSM Workspace'
    os.rename(os.path.join(BASE_DIR, 'workspace'), os.path.join(BASE_DIR, 'ADSM Workspace'))

user_settings_file = os.path.join(BASE_DIR, 'workspace.ini')
if not os.path.isfile(user_settings_file):
    Tk().withdraw()
    pick_custom_workspace = askyesno("Pick a custom location for your ADSM Workspace Directory?", 'Do you want to pick a custom location for your ADSM Workspace directory?\nIf not, your installation will be considered "Portable" and an ADSM Workspace folder will be created in the root of your installation.\n\nIf you are on a shared or networked computer and wish to share your ADSM Workspace with other users, then you should select a custom directory.')
    if pick_custom_workspace:
        custom_directory = askdirectory(initialdir=BASE_DIR, title="Select location for ADSM Workspace Directory", mustexist=True)
        custom_directory = os.path.join(custom_directory, 'ADSM Workspace')
        if not str(custom_directory).strip():
            custom_directory = "."
            Message(title="Notice!", message="You did not select a directory!\nDefaulting to a Portable installation in the root folder of this installation.").show()
    else:
        custom_directory = "."

    with open(user_settings_file, 'w') as user_settings:
        user_settings.write('WORKSPACE_PATH = %s' % json.dumps(custom_directory))

auto_settings_file = os.path.join(BASE_DIR, 'auto.ini')
if os.path.exists(auto_settings_file):
    os.remove(auto_settings_file)
if args.workspace_path:
    with open(auto_settings_file, 'w') as auto_settings:
        auto_settings.write('WORKSPACE_PATH = %s' % json.dumps(os.path.abspath(args.workspace_path)))

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
elif args.run_all_scenarios or args.exclude_scenarios or args.exclude_scenarios_list or args.run_scenarios or args.run_scenarios_list:
    management.call_command('auto',
                            run_all_scenarios=args.run_all_scenarios,
                            exclude_scenarios=args.exclude_scenarios,
                            exclude_scenarios_list=args.exclude_scenarios_list,
                            run_scenarios=args.run_scenarios,
                            run_scenarios_list=args.run_scenarios_list,
                            workspace_path=args.workspace_path,
                            output_path=args.output_path,
                            max_iterations=args.max_iterations)
elif args.workspace_path or args.output_path or args.max_iterations:
    raise ValueError('The command line arguments "workspace-path", "output-path", and "max-iterations" currently only work with the ADSM Auto Scenario Runner!')
else:
    # NOTE: Normally you would need to check for updates. However, graceful startup is doing this for us.
    try:
        server_port, app_port = find_available_ports()
    except:
        print("\nUnable to find a port to bind to! Cannot launch application.")
        print("\nPress any key to close the application...")
        input()
        # TODO: Find a way to close the browser if it is still alive.
        sys.exit(1)

    browser = threading.Timer(2, launch_viewer, [server_port, ])
    browser.start()

    print("\nLaunching server...")
    try:
        server_status = management.call_command('runproductionserver', port=server_port, app_port=app_port, silent=True)
        if server_status != 0:
            raise RuntimeError("Error launching Django Production Server!")
    except:
        if browser.is_alive():
            browser.cancel()
            print("It appears that the Django Production Server Application is either missing or not compatible with this system!\nADSM cannot run without a local server.\nPlease repair your installation.\n")
            print("\nPress any key to exit...")
            input()
            sys.exit(1)
