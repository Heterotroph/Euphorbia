from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from euphorbia import settings

__author__ = 'igorzygin'


@login_required
def home(request):
    return HttpResponseRedirect("/platform/tracking/")



def logout_view(request):
    logout(request)
    return HttpResponseRedirect("/")


def anonymous_required(func):
    def as_view(request, *args, **kwargs):
        redirect_to = kwargs.get('next', settings.LOGIN_REDIRECT_URL )
        if request.user.is_authenticated():
            return redirect(redirect_to)
        response = func(request, *args, **kwargs)
        return response
    return as_view