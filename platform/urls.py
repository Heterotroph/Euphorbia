from django.conf.urls import patterns, include, url
from platform.views import *

 
urlpatterns = patterns('',
    url(r'^profile/', profile),

    url(r'^tracking/', tracking),
    url(r'^tracking_ajax/', tracking_ajax),
    url(r'^sites/', tracking),
    url(r'^advert/', tracking),

    url(r'^login/', 'django.contrib.auth.views.login', {"template_name": "login.html"}),
    url(r'^logout/', logout_view),
    url(r'^register/', register)
)