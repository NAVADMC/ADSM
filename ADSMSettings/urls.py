from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url('^LoadingScreen/$', 'ADSMSettings.views.loading_screen'),
    url('^CheckUpdate/$', 'ADSMSettings.views.check_update'),
    url('^Update/$', 'ADSMSettings.views.update_adsm_from_git'),
    url('^SaveScenario/$', 'ADSMSettings.views.save_scenario'),
    url('^NewScenario/$', 'ADSMSettings.views.new_scenario'),
    url('^Workspace/$', 'ADSMSettings.views.file_dialog'),
    
    url(r'^ImportScenario/$', 'ADSMSettings.views.import_naadsm_scenario'),
    url(r'^OpenScenario/(?P<target>.+)/$', 'ADSMSettings.views.open_scenario'),  # includes .extension
    url(r'^DeleteFile/(?P<target>.+)/$', 'ADSMSettings.views.delete_file'),
    url(r'^Download/(?P<target>.+)/$', 'ADSMSettings.views.download_file'),
    url(r'^Copy/(?P<target>.+)/$', 'ADSMSettings.views.copy_file'),
    url(r'^Upload/$', 'ADSMSettings.views.upload_scenario'),
)