from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from future import standard_library
standard_library.install_hooks()
from django.contrib import admin
from django.db.models import get_models, get_app
from ScenarioCreator.models import RelationalFunction, RelationalPoint


class PointInline(admin.TabularInline):
    model = RelationalPoint
    extra = 2


class FunctionAdmin(admin.ModelAdmin):
    fields = ['name', 'x_axis_units', 'y_axis_units', 'notes']
    inlines = [PointInline]


for myModel in get_models(get_app("ScenarioCreator")):
    if myModel != RelationalFunction:
        admin.site.register(myModel)

admin.site.register(RelationalFunction, FunctionAdmin)