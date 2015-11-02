from django.forms import ModelForm
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from rotator.models import UserPixel, UserSite

__author__ = 'igor'

def pixel_form(request,site_id):
    site = UserSite.objects.get(pk=site_id)
    if request.method=="GET":
        context = {}
        return render_to_response("rotator/pixel_form.html", context=context, context_instance=RequestContext(request))
    if request.method=="POST":
        form = PixelForm(request.POST)
        if form.is_valid():
            pixel = UserPixel.objects.create(site = site)
            pixel.name = form.cleaned_data['name']
            pixel.unique_code = pixel.generate_unique_code()
            pixel.save()
            return HttpResponseRedirect('/rotator/sites/%d/' % site.id)
        context = {'form':form}
        return render_to_response("rotator/pixel_form.html", context=context, context_instance=RequestContext(request))

def pixel_form_edit(request, id):
    pixel = UserPixel.objects.filter(pk=id)[0]
    if request.method=="GET":
        context = {'form':PixelForm(instance=pixel)}
        return render_to_response("rotator/pixel_form_edit.html", context=context, context_instance=RequestContext(request))
    if request.method=="POST":
        form = PixelForm(request.POST)
        if form.is_valid():
            pixel.name = form.cleaned_data['name']
            pixel.save()
            return HttpResponseRedirect('/rotator/pixel/%d/' % pixel.id)
        context = {'form':form}
        return render_to_response("rotator/pixel_form_edit.html", context=context, context_instance=RequestContext(request))

def pixel_one_view(request, id):
    pixel=UserPixel.objects.get(pk=id)
    context = {'instance':pixel}
    return render_to_response("rotator/pixel_one_view.html", context=context, context_instance=RequestContext(request))


class PixelForm(ModelForm):
    class Meta:
        model = UserPixel
        fields = ['name']