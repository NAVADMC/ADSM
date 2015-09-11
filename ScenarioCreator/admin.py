from django.contrib import admin
from django.apps import apps
from ScenarioCreator.models import RelationalFunction, RelationalPoint


class PointInline(admin.TabularInline):
    model = RelationalPoint
    extra = 2


class FunctionAdmin(admin.ModelAdmin):
    fields = ['name', 'x_axis_units', 'y_axis_units', 'notes']
    inlines = [PointInline]

myapp = apps.get_app_config('ScenarioCreator')
for myModel in myapp.models.values():
    if myModel != RelationalFunction:
        admin.site.register(myModel)

admin.site.register(RelationalFunction, FunctionAdmin)