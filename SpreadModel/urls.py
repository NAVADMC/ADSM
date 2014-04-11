from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'SpreadModel.views.home', name='home'),
    url(r'^setup/', include('ScenarioCreator.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'ScenarioCreator.views.home'),
    url(r'^setup/$', 'ScenarioCreator.views.home'),
)
