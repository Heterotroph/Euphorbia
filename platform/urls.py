from django.conf.urls import patterns, url
from euphorbia.views import anonymous_required
from platform.views.adspots import OneAdspotView, CreateAdspotView
from platform.views.other import tracking, tracking_ajax, profile, logout_view, register
from platform.views.register import RegisterView
from django.contrib.auth import views
from django.views.generic import RedirectView
from platform.views.sites import SitesView, OneSiteView, CreateSiteView

__author__ = 'igorzygin'


urlpatterns = patterns('',
        url(r'^$', RedirectView.as_view(url='login/')),
        url(r'^profile/', profile),

        url(r'^tracking/', tracking),
        url(r'^tracking_ajax/', tracking_ajax),
        url(r'^sites/create/$', CreateSiteView.as_view()),
        url(r'^sites/(?P<pk>\d+)/$', OneSiteView.as_view()),
        url(r'^sites/', SitesView.as_view()),

        url(r'^adspots/create/$', CreateAdspotView.as_view()),
        url(r'^adspots/(?P<pk>\d+)/$', OneAdspotView.as_view()),

        url(r'^advert/', tracking),

        url(r'^register/',  anonymous_required(RegisterView.as_view())),
        url(r'^login/', anonymous_required(views.login), {"template_name": "registration/login.html"}),
        url(r'^logout/', logout_view),
        url(r'^register/', register)
    )