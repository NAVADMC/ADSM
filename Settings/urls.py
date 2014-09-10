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
    url('^SaveScenario/$', 'Settings.views.save_scenario'),
    url('^NewScenario/$', 'Settings.views.new_scenario'),
    url('^Workspace/$', 'Settings.views.file_dialog'),
    
    url(r'^OpenScenario/(?P<target>[\w\s\-\.]+)/$', 'Settings.views.open_scenario'),  # includes .extension
    url(r'^DeleteFile/(?P<target>.*)/$', 'Settings.views.delete_file'),
    url(r'^Download/(?P<target>[\w\s\-\./]+)/$', 'Settings.views.download_file'),
    url(r'^Copy/(?P<target>[\w\s\-\.]+)/$', 'Settings.views.copy_file'),
    url(r'^Upload/$', 'Settings.views.upload_scenario'),
)