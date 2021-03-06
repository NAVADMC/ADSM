from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url('^Startup/$', 'ADSMSettings.views.startup'),
    url('^Update/$', 'ADSMSettings.views.update_adsm_from_git'),
    url('^SaveScenario/$', 'ADSMSettings.views.save_scenario'),
    url('^NewScenario/(?P<new_name>.*)$', 'ADSMSettings.views.new_scenario'),
    url('^Workspace/$', 'ADSMSettings.views.file_dialog'),
    url('^Backend/$', 'ADSMSettings.views.backend', {'url': "/admin/"}),
    url('^SQLBackend/$', 'ADSMSettings.views.backend', {'url': "/explorer"}),
    url('^ShowHelpText.json/$', 'ADSMSettings.views.show_help_text_json'),
    url('^ShowHelpOverlay.json/$', 'ADSMSettings.views.show_help_overlay_json'),

    url(r'^ImportScenario/(?P<new_name>.*)$', 'ADSMSettings.views.import_naadsm_scenario'),
    url(r'^ImportStatus/$', 'ADSMSettings.views.import_status'),
    url(r'^OpenScenario/(?P<target>.+)/$', 'ADSMSettings.views.open_scenario'),  # includes .extension
    url(r'^OpenTestScenario/(?P<target>.+)/$', 'ADSMSettings.views.open_test_scenario'),  # includes .extension
    url(r'^DeleteFile/(?P<target>.+)/$', 'ADSMSettings.views.delete_file'),
    url(r'^Download/$', 'ADSMSettings.views.download_file'),
    url(r'^Copy/(?P<target>.+)/(?P<destination>.+)/$', 'ADSMSettings.views.copy_file'),
    url(r'^Upload/$', 'ADSMSettings.views.upload_scenario'),

    url(r'^DeleteWorkspaceSetting/$', 'ADSMSettings.views.delete_workspace_setting')
)