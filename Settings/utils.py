from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from future import standard_library

standard_library.install_hooks()

from django.db import connections

def close_all_connections():
    for conn in connections:
        connections[conn].close()
