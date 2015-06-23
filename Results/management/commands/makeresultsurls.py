import os
import re

from django.core.management.base import BaseCommand
from django.conf import settings
from django.conf.urls import patterns, url  # do not delete this

from ScenarioCreator.models import *  # do not delete this
from ScenarioCreator.forms import *  # do not delete this


class Command(BaseCommand):
    """Assumes that the only classes in models.py are models.Model.  Because any class will be given a URL,
    whether it is a model or not."""
    @staticmethod
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
        return output

    def handle(self, *args, **options):
        urls_path = os.path.join(settings.BASE_DIR, 'Results', 'urls.py')
        if os.path.isfile(urls_path):
            os.remove(urls_path)

        urlpatterns = self.generate_urls_from_models(os.path.join(settings.BASE_DIR, 'Results','models.py'),
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
                                                      "url('^abort_simulation$', 'Results.utils.abort_simulation')",
                                                      ])

        urls_code = "\"\"\"URLs is entirely procedural based on the contents of models.py. This has the advantage that urls automatically update as the models change or are renamed.\"\"\"\n\n" \
                    "from django.conf.urls import patterns, url\n\n" \
                    "urlpatterns = " + urlpatterns

        urls_file = open(urls_path, 'w')
        urls_file.writelines(urls_code)
        urls_file.close()
