__author__ = 'josiahseaman'

from django.conf.urls import patterns, url
from ScenarioCreator.models import *
from ScenarioCreator.forms import *

urlpatterns = patterns('',
                       url('^$', "ScenarioCreator.views.new_scenario"),
                       url('^new/$', "ScenarioCreator.views.new_scenario",),

                       url('^DynamicUnit/new/$', "ScenarioCreator.views.new_entry"),
                       url('^DynamicUnit/(?P<primary_key>\d+)/$', "ScenarioCreator.views.edit_entry"),
                       )


