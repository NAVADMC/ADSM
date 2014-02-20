from django.contrib import admin
from django.db.models import get_models, get_app

modelsList = []

# Register your models here.
for myModel in get_models(get_app("ScenarioCreator")):
    admin.site.register(myModel)