__author__ = 'josiahseaman'

from django.conf.urls import patterns, url
urlpatterns = patterns('',
                       url('^$', "ScenarioCreator.views.start_window"))


