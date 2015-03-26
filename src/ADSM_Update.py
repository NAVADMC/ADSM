import os
import sys
import subprocess
import shutil
from time import sleep


print("Importing Python dependencies and setting local path...")

if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(os.path.dirname(sys.executable))
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

sleep(3)

os.chdir(os.path.join(BASE_DIR, 'src'))

if (getattr(sys, 'frozen', False) and 'update.now' in str(sys.executable).lower()) or (not getattr(sys, 'frozen', False) and 'update.now' in str(__file__).lower()):
    # Discretely import django items
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ADSM.settings")

    exec("import django")
    django.setup()
    exec("from django.conf import settings")
    exec("from ADSMSettings.utils import update_adsm")

    # This will always complain in an editor. Ignore it.
    update_adsm()

    UPDATE_PROGRAM = os.path.join(BASE_DIR, 'bin', 'adsm_update.exe')
    subprocess.Popen(UPDATE_PROGRAM)
    sys.exit()
else:
    if os.path.exists(os.path.join(BASE_DIR, 'bin', 'adsm_update.now.exe')):
        os.remove(os.path.join(BASE_DIR, 'bin', 'adsm_update.now.exe'))

        MAIN_PROGRAM = os.path.join(BASE_DIR, 'adsm.exe')
        subprocess.Popen(MAIN_PROGRAM)
        sys.exit()
    else:
        shutil.copy(os.path.join(BASE_DIR, 'bin', 'adsm_update.exe'), os.path.join(BASE_DIR, 'bin', 'adsm_update.now.exe'))

        UPDATE_PROGRAM = os.path.join(BASE_DIR, 'bin', 'adsm_update.now.exe')
        subprocess.Popen(UPDATE_PROGRAM)
        sys.exit()
