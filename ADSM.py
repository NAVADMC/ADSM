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
parser.add_argument('-s', '--skip_update', dest='skip_update', help='do not check for updates', action='store_true')
parser.add_argument('-n', '--update_name', dest='update_name', help='Query for the name of this program as known to the update server', action='store_true')
args = parser.parse_args()

print("Checking with the update service...")
# Update the updater
if os.path.exists(os.path.join(BASE_DIR, 'npu.exe.updated')):
    if os.path.exists(os.path.join(BASE_DIR, 'npu.exe')):
        os.remove(os.path.join(BASE_DIR, 'npu.exe'))
    os.rename(os.path.join(BASE_DIR, 'npu.exe.updated'), os.path.join(BASE_DIR, 'npu.exe'))
# Respond to an updater query
if args.update_name:
    print("ADSM")
    sys.exit(0)

print("Preparing Django environment...")

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ADSM.settings")

import django
django.setup()
from django.conf import settings
from django.core import management

if args.test:
    print("Running tests...")
    management.call_command('test')
else:
    browser = threading.Timer(.5, launch_viewer)
    browser.start()

    print("Launching server...")
    management.call_command('runproductionserver', port=8000, app_port=8001)
    # management.call_command('runserver', use_reloader=False)
