from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
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
    url(r'react/$', TemplateView.as_view(template_name='react.html')),
    static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)  # NOTE: This is usually dangerous... however, when in the production server mode, the Nginx server will intercept the static url first. It does open a security vulnerability if an attacker knows the app server port that is behind the Nginx server port; though one would hope that a client is behind a firewall.
    )

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += patterns('', url(r'^__debug__/', include(debug_toolbar.urls)), )

handler400 = 'ADSM.debug_views.handler400'
handler403 = 'ADSM.debug_views.handler403'
handler404 = 'ADSM.debug_views.handler404'
handler500 = 'ADSM.debug_views.handler500'  # TODO: Get these to show up when in debug!
