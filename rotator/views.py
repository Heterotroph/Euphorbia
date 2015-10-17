import random
from django.forms import ModelForm
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from rotator.models import Banner, UserSite

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



def sites_list(request):
    sites_list = UserSite.objects.filter(user=request.user)
    context = {'sites_list':sites_list}
    return render_to_response("rotator/sites_list.html", context=context)

def sites_form(request):
    if request.method=="GET":
        context = {}
        return render_to_response("rotator/sites_form.html", context=context, context_instance=RequestContext(request))
    if request.method=="POST":
        form = SiteForm(request.POST)
        if form.is_valid():
            site = UserSite.objects.create(user = request.user)
            site.name = form.cleaned_data['name']
            site.url = form.cleaned_data['url']
            site.save()
            return HttpResponseRedirect('/rotator/sites/')
        context = {'form':form}
        return render_to_response("rotator/sites_form.html", context=context, context_instance=RequestContext(request))

def sites_form_edit(request, id):
    site=UserSite.objects.get(pk=id)
    if request.method=="GET":
        context = {}
        context['form']=SiteForm(instance=site)
        return render_to_response("rotator/sites_form_edit.html", context=context, context_instance=RequestContext(request))
    if request.method=="POST":
        form = SiteForm(request.POST)
        if form.is_valid():
            site.name = form.cleaned_data['name']
            site.url = form.cleaned_data['url']
            site.save()
            return HttpResponseRedirect('/rotator/sites/')
        context = {'form':form}
        return render_to_response("rotator/sites_form_edit.html", context=context, context_instance=RequestContext(request))


def sites_one_view(request, id):
    site=UserSite.objects.get(pk=id)
    context = {'instance':site}
    return render_to_response("rotator/sites_one_view.html", context=context, context_instance=RequestContext(request))


class SiteForm(ModelForm):
    class Meta:
        model = UserSite
        fields = ['name', 'url']