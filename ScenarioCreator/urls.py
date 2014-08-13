"""URLs is entirely procedural based on the contents of models.py.
This has the advantage that urls automatically update as the models change or are renamed."""
from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from future.builtins import open
from future import standard_library
standard_library.install_hooks()

import re

__author__ = 'josiahseaman'

from django.conf.urls import patterns, url  # do not delete this
from ScenarioCreator.models import *  # do not delete this
from ScenarioCreator.forms import *  # do not delete this


"""Assumes that the only classes in models.py are models.Model.  Because any class will be given a URL,
whether it is a model or not."""
def generate_urls_from_models(input_file, extra_urls=()):
    assert hasattr(extra_urls, '__getitem__')
    lines = open(input_file, 'r').readlines()
    model_strings = extra_urls  # extra_urls is placed first so that they take precedence over auto-urls
    for line in lines:
        if 'class' in line[:5]:
            model_name = re.split('\W+', line)[1]
            model_strings.append("url('^" + model_name + "/$',                      'ScenarioCreator.views.model_list')")
            model_strings.append("url('^" + model_name + "/new/$',                  'ScenarioCreator.views.new_entry')")
            model_strings.append("url('^" + model_name + "/(?P<primary_key>\d+)/$', 'ScenarioCreator.views.edit_entry')")
            model_strings.append("url('^" + model_name + "/(?P<primary_key>\d+)/copy/$', 'ScenarioCreator.views.copy_entry')")
            model_strings.append("url('^" + model_name + "/(?P<primary_key>\d+)/delete/$', 'ScenarioCreator.views.delete_entry')")

    output = "patterns('', " + ",\n         ".join(model_strings) + ")"
    return eval(output)


urlpatterns = generate_urls_from_models('ScenarioCreator/models.py',
                                        ["url('^AssignSpreads/$', 'ScenarioCreator.views.disease_spread')",
                                         "url('^AssignProtocols/$', 'ScenarioCreator.views.assign_protocols')",
                                         "url('^AssignProgressions/$', 'ScenarioCreator.views.assign_progressions')",
                                         "url('^AssignZoneEffects/$', 'ScenarioCreator.views.zone_effects')",
                                         

                                         "url('^Populations/$', 'ScenarioCreator.views.population')",
                                         "url('^UploadPopulation/$', 'ScenarioCreator.views.upload_population')",

                                         "url('^SaveScenario/$', 'ScenarioCreator.views.save_scenario')",
                                         "url('^NewScenario/$', 'ScenarioCreator.views.new_scenario')",
                                         "url('^Workspace/$', 'ScenarioCreator.views.file_dialog')",
                                         "url('^ValidateScenario/$', 'ScenarioCreator.views.validate_scenario')",

                                         "url('^OpenScenario/(?P<target>[\w\s\-\.]+)/$', 'ScenarioCreator.views.open_scenario')",  # includes .extension
                                         r"url('^DeleteFile/(?P<target>.*)/$', 'ScenarioCreator.views.delete_file')",
                                         r"url('^Download/(?P<target>[\w\s\-\./]+)/$', 'ScenarioCreator.views.download_file')",
                                         "url('^Copy/(?P<target>[\w\s\-\.]+)/$', 'ScenarioCreator.views.copy_file')",
                                         "url('^Upload/$', 'ScenarioCreator.views.upload_scenario')",
                                        ])

