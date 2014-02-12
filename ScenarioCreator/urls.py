__author__ = 'josiahseaman'

from django.conf.urls import patterns, url
urlpatterns = patterns('',
                       url('^$', "ScenarioCreator.views.start_window"),
                       url('^new/$', "ScenarioCreator.views.new_scenario"),
                       url('^(?P<primary_key>\d+)/$', "ScenarioCreator.views.edit_scenario"),
                       )


