import os
import sys
import subprocess


print("Importing Python dependencies and setting local path...")

if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(sys.executable)
    sys.path.append(os.path.join(BASE_DIR, 'src'))
    os.environ["PATH"] += os.pathsep + os.path.join(BASE_DIR, 'bin')
else:
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(BASE_DIR)

os.chdir(BASE_DIR)


def path_all_the_eggs():
    packages = os.path.join(BASE_DIR, "Lib", "site-packages")
    for folder in os.listdir(packages):
        subfolder = os.path.join(packages, folder)
        if os.path.isdir(subfolder):
            if folder[-4:] == '.egg':
                sys.path.append(subfolder)

sys.path.append(BASE_DIR)
sys.path.append(os.path.join(BASE_DIR, "DLLs"))
sys.path.append(os.path.join(BASE_DIR, "Lib"))
sys.path.append(os.path.join(BASE_DIR, "Lib", "plat-win"))
sys.path.append(os.path.join(BASE_DIR, "Lib", "lib-tk"))
sys.path.append(os.path.join(BASE_DIR, "Lib", "site-packages"))
sys.path.append(os.path.join(BASE_DIR, "bin"))
sys.path.append(os.path.join(BASE_DIR, "Scripts"))
path_all_the_eggs()

import multiprocessing
multiprocessing.freeze_support()
import argparse

import threading
import _thread
from collections import UserDict, UserList, UserString
from collections import MutableMapping as DictMixin
import decimal
import contextlib
import json
import hmac
import cgi
from logging import handlers
import xml.dom.minidom
import wsgiref
from wsgiref import simple_server
import sqlite3
import xml.etree.ElementTree
import ast
from concurrent.futures import ProcessPoolExecutor
import distutils.version
from distutils import command
import csv
import uuid
import distutils.util
import email.mime
import email.mime.text
import email.mime.multipart
import email.mime.message
import http.cookies
import html.entities
from html import parser as html_parser
import logging.config
import _pyio
import ctypes.wintypes


def launch_viewer():
    subprocess.call(os.path.join(BASE_DIR, 'Viewer', 'ADSM Viewer.exe'))
    print("Closing application!")
    _thread.interrupt_main()


parser = argparse.ArgumentParser(prog='ADSM.exe')
parser.add_argument('-t', '--test', dest='test', help='run the test suite', action='store_true')
parser.add_argument('-s', '--skip_update', dest='skip_update', help='do not check for updates', action='store_true')
args = parser.parse_args()


print("Preparing Django environment...")

os.chdir(os.path.join(BASE_DIR, "src"))

if os.path.exists(os.path.join(BASE_DIR, 'bin', 'adsm_update.now.exe')):
    os.remove(os.path.join(BASE_DIR, 'bin', 'adsm_update.now.exe'))
if os.path.exists(os.path.join(BASE_DIR, 'bin', 'adsm_force_reset_and_update.now.exe')):
    os.remove(os.path.join(BASE_DIR, 'bin', 'adsm_force_reset_and_update.now.exe'))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ADSM.settings")

exec("import django")
django.setup()
exec("from django.conf import settings")
exec("from django.core import management")

if not args.skip_update:
    exec("from ADSMSettings.utils import update_requested")
    if update_requested():
        UPDATE_PROGRAM = os.path.join(BASE_DIR, 'bin', 'adsm_update.exe')
        subprocess.Popen(UPDATE_PROGRAM)
        sys.exit()


if args.test:
    management.call_command('test')
else:
    browser = threading.Timer(3, launch_viewer)
    browser.start()

    management.call_command('runproductionserver', port=8000, app_port=8001)
