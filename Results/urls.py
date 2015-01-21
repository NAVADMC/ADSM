"""URLs is entirely procedural based on the contents of models.py.
This has the advantage that urls automatically update as the models change or are renamed."""
__author__ = 'josiahseaman'

import re
from django.conf import settings
from django.conf.urls import patterns, url  # do not delete this
from Results.models import *  # do not delete this


"""Assumes that the only classes in models.py are models.Model.  Because any class will be given a URL,
whether it is a model or not."""
def generate_urls_from_models(input_file, extra_urls=()):
    assert hasattr(extra_urls, '__getitem__')
    lines = open(input_file, 'r').readlines()
    model_strings = extra_urls  # extra_urls is placed first so that they take precedence over auto-urls
    for line in lines:
        if 'class' in line[:5]:
            model_name = re.split('\W+', line)[1]
            model_strings.append("url('^" + model_name + "/$',                          'Results.views.model_list')")
            model_strings.append("url('^" + model_name + "/prefix/(?P<prefix>\w{1,4})/$',  'Results.views.filtered_list')")
            # model_strings.append("url('^" + model_name + "/(?P<primary_key>\d+)/$', 'Results.views.edit_entry')")

    output = "patterns('', " + ",\n         ".join(model_strings) + ")"
    return eval(output)


urlpatterns = generate_urls_from_models(
    os.path.join(settings.BASE_DIR, 'Results','models.py'),
    ["url('^$', 'Results.views.results_home')",
     "url('^RunSimulation/$', 'Results.views.run_simulation')",
     "url('^Population\.png$', 'Results.graphing.population_png')",
     "url('^population_d3_map/$', 'Results.interactive_graphing.population_d3_map')",
     "url('^population_thumbnail\.png$', 'Results.interactive_graphing.population_thumbnail_png')",
     "url('^population_zoom\.png$', 'Results.interactive_graphing.population_zoom_png')",
     "url('^(?P<model_name>\w+)/(?P<field_name>\w+)/(?P<iteration>\d*)/?$', 'Results.views.graph_field')",  # optional iteration argument
     "url('^(?P<model_name>\w+)/(?P<field_name>\w+)/(?P<iteration>\d*)/?(?P<zone>[^/]*)/?Graph\.png$', 'Results.graphing.graph_field_png')",
     "url('^Inputs/$', 'Results.views.back_to_inputs')",
     "url('^simulation_status.json$', 'Results.views.simulation_status')",
     "url('^abort_simulation$', 'Results.models.abort_simulation')",  # I know it should be in views, figure out a non-circular import
     ])

