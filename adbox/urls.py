from django.conf.urls import patterns, include, url
from adboxweb.views import *
from django.contrib import admin
 
urlpatterns = patterns('',
    url(r'^$', 'django.contrib.auth.views.login'),
    url(r'^accounts/profile/', home),
    url(r'^logout/$', logout_view),
    # url(r'^login/$', 'django.contrib.auth.views.login'), # If user is not login it will redirect to login page
    # url(r'^register/$', register),
    # url(r'^register/success/$', register_success),
    # url(r'^home/$', home),
    # url(r'^admin/', include(admin.site.urls)),
    # url(r'^banner/new/', new_banner),
    #
    url(r'^platform/tracking/', tracking),
    url(r'^platform/tracking_ajax/', tracking_ajax),
    url(r'^platform/sites/', tracking),
    url(r'^platform/advert/', tracking),
    url(r'^platform/profile/', tracking),
    url(r'^platform/login/', tracking),
    url(r'^platform/', tracking),
    #
    # url(r'^campaigns/', campaign_list),
    # url(r'^campaign/new/', new_campaign),
    # url(r'^publisher/register', register_publisher, name='register_publisher'),
    # url(r'^advertizer/register', register_advertizer, name='register_advertizer'),

    # url(r'^faq/', faq),
    # url(r'^instructions/', instructions),
    # url(r'^conditions/', conditions),
    # url(r'^formats/', formats),
    # url(r'^thanks/', thanks),
    # url(r'^rotator/', include('rotator.urls', namespace="user")),
)