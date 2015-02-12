import os
import sys
import subprocess
from time import sleep


print("Importing Python dependencies and setting local path...")

if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(os.path.dirname(sys.executable))
    sys.path.append(os.path.join(BASE_DIR, 'src'))
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

def forceful_git_cleanup():
    import psutil
    print("Kill all git processes")
    for process in psutil.process_iter():
        try:
            if 'git' in process.name():
                process.kill()
                # make sure it's dead
        except (psutil.AccessDenied, PermissionError) as e:
            pass  # print("IMPORTANT: Run this program again as administrator if this doesn't work.", e)
        
    lock_file = os.path.join(BASE_DIR, ".git", "index.lock")
    if os.path.exists(lock_file):
        try:
            os.remove(lock_file)
        except:
            print("IMPORTANT: You will need to manually delete ", lock_file, "before ADSM can update.")
            sleep(10)
            quit()
            
forceful_git_cleanup()

os.chdir(os.path.join(BASE_DIR, "src"))

# Discretely import django items
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ADSM.settings")

exec("import django")
django.setup()
exec("from django.conf import settings")
exec("from ADSMSettings.utils import reset_and_update_adsm")

reset_and_update_adsm()# This will always complain in an editor. Ignore it.

quit()
