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
    # Examples:
    # url(r'^$', 'SpreadModel.views.home', name='home'),
    url(r'^setup/', include('ScenarioCreator.urls')),
    url(r'^results/', include('Results.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'ScenarioCreator.views.home'),
    url(r'^setup/$', 'ScenarioCreator.views.home'),
)
