from django.apps import apps
from django.contrib import admin

# Register your models here.
myapp = apps.get_app_config('ADSMSettings')
for myModel in myapp.models.values():
    admin.site.register(myModel)