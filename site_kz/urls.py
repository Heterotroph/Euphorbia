from django.conf.urls import patterns, include, url
from views import *

urlpatterns = patterns('',

    url(r'^$', index, name='index'),
    url(r'^publisher/register', register_publisher, name='register_publisher'),
    url(r'^advertizer/register', register_advertizer, name='register_advertizer'),

)
