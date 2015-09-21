import random
from django.shortcuts import render_to_response
from django.template import RequestContext
from rotator.models import Banner

__author__ = 'igorzygin'


def get_banner(request):
    banners = Banner.objects.all()
    r = int(random.random()*(len(banners)-1))
    selected_banner=list(banners)[r]
    variables = RequestContext(request,
                               {
        'img': selected_banner.banner_url
    })
    return render_to_response('rotator/rotator.html',variables)