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
    )

handler500 = 'ADSMSettings.views.handler500'