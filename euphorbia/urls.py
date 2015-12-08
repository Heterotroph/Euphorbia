from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import RedirectView
from euphorbia import settings
from euphorbia.views import home, logout_view, anonymous_required
from django.contrib.auth import views



urlpatterns = patterns('',
        url(r'^$', RedirectView.as_view(url='/platform/login/')),
        url(r'^logout/$', logout_view),
        url(r'^admin/', include(admin.site.urls)),
        url(r'^platform/', include('platform.urls', namespace="platform")),
        url(r'^favicon\.ico$', RedirectView.as_view(url='/static/img/logos/favicon.ico'))
    ) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)