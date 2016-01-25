from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from django.contrib import admin
from django.conf import settings


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
    url(r'react/$', TemplateView.as_view(template_name='react.html'))
    )

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += patterns('', url(r'^__debug__/', include(debug_toolbar.urls)), )

handler400 = 'ADSM.debug_views.handler400'
handler403 = 'ADSM.debug_views.handler403'
handler404 = 'ADSM.debug_views.handler404'
handler500 = 'ADSM.debug_views.handler500'  # TODO: Get these to show up when in debug!
