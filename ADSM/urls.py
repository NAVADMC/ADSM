from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^setup/', include('ScenarioCreator.urls')),
    url(r'^results/', include('Results.urls')),
    url(r'^app/', include('ADSMSettings.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'ADSMSettings.views.home'),
    url('^LoadingScreen/$', 'ADSMSettings.views.loading_screen'),
    url('^500/$', 'ADSM.debug_views.handler500'),
    )

handler400 = 'ADSM.debug_views.handler400'
handler403 = 'ADSM.debug_views.handler403'
handler404 = 'ADSM.debug_views.handler404'
handler500 = 'ADSM.debug_views.handler500'  # TODO: Get these to show up when in debug!
