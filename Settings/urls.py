from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from future import standard_library
standard_library.install_hooks()
from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',

    url(r'^update/$', 'Settings.views.update_adsm_from_git'),
    url('^SaveScenario/$', 'ScenarioCreator.views.save_scenario'),
    url('^NewScenario/$', 'ScenarioCreator.views.new_scenario'),
    url('^Workspace/$', 'ScenarioCreator.views.file_dialog'),
    
    url(r'^OpenScenario/(?P<target>[\w\s\-\.]+)/$', 'ScenarioCreator.views.open_scenario'),  # includes .extension
    url(r'^DeleteFile/(?P<target>.*)/$', 'ScenarioCreator.views.delete_file'),
    url(r'^Download/(?P<target>[\w\s\-\./]+)/$', 'ScenarioCreator.views.download_file'),
    url(r'^Copy/(?P<target>[\w\s\-\.]+)/$', 'ScenarioCreator.views.copy_file'),
    url(r'^Upload/$', 'ScenarioCreator.views.upload_scenario'),
)