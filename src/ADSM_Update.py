import os
import sys
import subprocess
from time import sleep


print("Importing Python dependencies and setting local path...")

if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.join(os.path.dirname(os.path.dirname(sys.executable)), 'src')
    os.environ["PATH"] += os.pathsep + os.path.join(os.path.dirname(BASE_DIR), 'bin')
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
print(BASE_DIR)
TOP_DIR = os.path.dirname(BASE_DIR)

os.chdir(BASE_DIR)


def path_all_the_eggs():
    packages = os.path.join(TOP_DIR, "Lib", "site-packages")
    for folder in os.listdir(packages):
        subfolder = os.path.join(packages, folder)
        if os.path.isdir(subfolder):
            if folder[-4:] == '.egg':
                sys.path.append(subfolder)

sys.path.append(BASE_DIR)
sys.path.append(os.path.join(TOP_DIR, "DLLs"))
sys.path.append(os.path.join(TOP_DIR, "Lib"))
sys.path.append(os.path.join(TOP_DIR, "Lib", "plat-win"))
sys.path.append(os.path.join(TOP_DIR, "Lib", "lib-tk"))
sys.path.append(os.path.join(TOP_DIR, "Lib", "site-packages"))
sys.path.append(os.path.join(TOP_DIR, "bin"))
sys.path.append(os.path.join(TOP_DIR, "Scripts"))
path_all_the_eggs()

sleep(5)

# Discretely import django items
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ADSM.settings")

exec("import django")
django.setup()
exec("from django.conf import settings")
exec("from ADSMSettings.utils import update_adsm")

# This will always complain in an editor. Ignore it.
update_adsm()

MAIN_PROGRAM = os.path.join(os.path.dirname(BASE_DIR), 'ADSM.exe --skip_update')
subprocess.Popen(MAIN_PROGRAM)
sys.exit()
