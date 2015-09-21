from rotator.views import get_banner

__author__ = 'igorzygin'



from django.conf.urls import patterns, include, url


urlpatterns = patterns('/',
    # url(r'^$', index),
    url(r'^$', get_banner),

)
