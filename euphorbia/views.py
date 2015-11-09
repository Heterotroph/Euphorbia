from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect

__author__ = 'igorzygin'


@login_required
def home(request):
    return HttpResponseRedirect("/platform/tracking/")



def logout_view(request):
    logout(request)
    return HttpResponseRedirect("/")