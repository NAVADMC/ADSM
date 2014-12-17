"""URLs is entirely procedural based on the contents of models.py.
This has the advantage that urls automatically update as the models change or are renamed."""

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
                                         ["url('^AssignSpreads/$', 'ScenarioCreator.views.assign_disease_spread')",
                                         "url('^AssignProtocols/$', 'ScenarioCreator.views.assign_protocols')",
                                         "url('^AssignProgressions/$', 'ScenarioCreator.views.assign_progressions')",
                                         "url('^AssignZoneEffects/$', 'ScenarioCreator.views.zone_effects')",

                                         "url('^Populations/$', 'ScenarioCreator.views.population')",
                                         "url('^Population/new/$', 'ScenarioCreator.views.population')",  # force redirect for special singleton
                                         "url('^UploadPopulation/$', 'ScenarioCreator.views.upload_population')",
                                         "url('^ValidateScenario/$', 'ScenarioCreator.views.validate_scenario')",
                                        ])

