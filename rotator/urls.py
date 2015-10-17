from rotator.views import get_banner, sites_list, sites_form, sites_form_edit, sites_one_view

__author__ = 'igorzygin'



from django.conf.urls import patterns, include, url


urlpatterns = patterns('/',
    # url(r'^$', index),
    url(r'^sites/create/', sites_form),
    url(r'^sites/edit/(?P<id>[0-9]+)/', sites_form_edit),
    url(r'^sites/(?P<id>[0-9]+)/', sites_one_view),
    url(r'^sites/', sites_list),



)
