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
    key = "DJANGO_SETTINGS_MODULE"
    value = "SpreadModel.settings"
    if os.name == 'nt':
        key = key.encode('ascii', 'ignore')
        value = value.encode('ascii', 'ignore')
    os.environ.setdefault(key, value)

    main(sys.argv)
