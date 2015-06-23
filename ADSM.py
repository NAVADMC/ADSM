import os
import sys
import subprocess
import multiprocessing
import argparse
import threading
import _thread

multiprocessing.freeze_support()


def launch_viewer():
    print("Launching browser...")
    subprocess.call(os.path.join(BASE_DIR, 'Viewer', 'ADSM Viewer.exe'))
    print("Closing application!")
    _thread.interrupt_main()


print("Setting up Python...")

if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
print(BASE_DIR)

os.chdir(BASE_DIR)

print("Preparing Django environment...")

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ADSM.settings")

import django
django.setup()
from django.conf import settings
from django.core import management

parser = argparse.ArgumentParser(prog='adsm.exe')
parser.add_argument('-t', '--test', dest='test', help='run the test suite', action='store_true')
parser.add_argument('-s', '--skip_update', dest='skip_update', help='do not check for updates', action='store_true')
args = parser.parse_args()

if args.test:
    print("Running tests...")
    management.call_command('test')
else:
    browser = threading.Timer(.5, launch_viewer)
    browser.start()

    print("Launching server...")
    management.call_command('runproductionserver', port=8000, app_port=8001)
    # management.call_command('runserver', use_reloader=False)
