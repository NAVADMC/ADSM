import os
import sys
import auto_runner
from django.core.management import execute_from_command_line


if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

sys.path.append(BASE_DIR)


def main(*args):
    # if at least one user-command line argument is given (first args is always this file's location)
    if(len(args[0]) > 1):
        # if the first given argument is --auto
        if(args[0][1] == "--auto"):
            # start the ADSM auto-runner
            auto_runner.setup(*args)
            # return, so ADSM does not also start normally
            return 0

    execute_from_command_line(*args)

if __name__ == "__main__":
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ADSM.settings')

    main(sys.argv)
