from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import RedirectView
from euphorbia.views import home, logout_view, anonymous_required
from django.contrib.auth import views


urlpatterns = patterns('',
        url(r'^$', RedirectView.as_view(url='/platform/login/')),
        url(r'^logout/$', logout_view),
        url(r'^admin/', include(admin.site.urls)),
        url(r'^platform/', include('platform.urls', namespace="platform")),
    )