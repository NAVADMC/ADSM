from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from future import standard_library
standard_library.install_hooks()
from django.contrib import admin
from django.db.models import get_models, get_app

# Register your models here.
for myModel in get_models(get_app("Settings")):
    admin.site.register(myModel)