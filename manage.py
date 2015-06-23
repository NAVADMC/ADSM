import os
import sys
from django.core.management import execute_from_command_line


if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(sys.executable), 'src'
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

sys.path.append(BASE_DIR)


def main(*args):
    execute_from_command_line(*args)

if __name__ == "__main__":
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ADSM.settings')

    main(sys.argv)
