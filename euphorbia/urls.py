from django.conf.urls import patterns, include, url
from django.contrib import admin
import platform
 
urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^platform/', include('platform.urls')),
)