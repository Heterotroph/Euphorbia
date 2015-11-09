from django.conf.urls import patterns, url
from euphorbia.views import anonymous_required
from platform.views.other import tracking, tracking_ajax
from platform.views.register import RegisterView

__author__ = 'igorzygin'


urlpatterns = patterns('',
                        url(r'^register/',  anonymous_required(RegisterView.as_view())),
                        url(r'^tracking/', tracking),
                        url(r'^tracking_ajax/', tracking_ajax),
                        url(r'^sites/', tracking),
                        url(r'^advert/', tracking),
                        url(r'^profile/', tracking),
                        url(r'^login/', tracking),


                  )