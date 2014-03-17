#!/usr/bin/env python
import os
import sys
from django.core.management import execute_from_command_line

def main(*args):

    execute_from_command_line(*args)

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SpreadModel.settings")

    main(sys.argv)
