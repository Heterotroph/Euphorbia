from django.conf.urls import patterns, include, url
from django.contrib import admin
from euphorbia.views import home, logout_view

urlpatterns = patterns('',
    url(r'^$', 'django.contrib.auth.views.login'),
    url(r'^accounts/profile/', home),
    url(r'^logout/$', logout_view),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^platform/', include('platform.urls', namespace="platform")),
    url(r'^/', include('platform.urls', namespace="platform")),
)