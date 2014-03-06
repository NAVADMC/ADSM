"""URLs is entirely procedural based on the contents of models.py.
This has the advantage that urls automatically update as the models change or are renamed."""

import re

__author__ = 'josiahseaman'

from django.conf.urls import patterns, url
from ScenarioCreator.models import *
from ScenarioCreator.forms import *


"""Assumes that the only classes in models.py are models.Model.  Because any class will be given a URL,
whether it is a model or not."""
def generate_urls_from_models(input_file):
    lines = open(input_file, 'r').readlines()
    model_strings = []
    for line in lines:
        if 'class' in line[:5]:
            model_name = re.split('\W+', line)[1]
            model_strings.append("url('^" + model_name + "/new/$', 'ScenarioCreator.views.new_entry')")
            model_strings.append("url('^" + model_name + "/(?P<primary_key>\d+)/$', 'ScenarioCreator.views.edit_entry')")

    output = "patterns('', " + ",\n         ".join(model_strings) + ")"
    return eval(output)


urlpatterns = generate_urls_from_models('ScenarioCreator/models.py')

