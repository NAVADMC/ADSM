#!/usr/bin/env python
from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from future import standard_library
standard_library.install_hooks()
import os
import sys
from django.core.management import execute_from_command_line

def main(*args):

    execute_from_command_line(*args)

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SpreadModel.settings")

    main(sys.argv)
