# -*- coding: utf-8 -*-

import json
from django import forms
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView, FormView
from platform.models import UserSite, AdSpot, AdThematics, AdFormat
from platform.views.sites import LoginRequiredMixin

__author__ = 'igorzygin'

def validate_adspot_name(value):
    if len(AdSpot.objects.filter(name=value))>0:
        raise ValidationError('%s must be unique' % value)

class OneAdspotView(LoginRequiredMixin, TemplateView):
    template_name = 'adspot_one.html'

    def get_context_data(self, **kwargs):
        pk=self.kwargs['pk']
        data = super(OneAdspotView, self).get_context_data(**kwargs)
        data['adspot'] = AdSpot.objects.get(pk=pk, site__user=self.request.user)
        print data['adspot']
        return data

#
#
class CreateAdspotView(LoginRequiredMixin, FormView):
    template_name = 'adspot_create.html'

    def get_format(self, request):
        return AdFormat.objects.all()

    def get_sites(self, request):
        return UserSite.objects.filter(user=request.user)


    def get(self, request, **kwargs):
        if request.user.is_anonymous():
            return HttpResponseRedirect("/")
        return self.render_to_response({"form": AdspotForm(), "format_choice":self.get_format(request), "site_choice":self.get_sites(request)})

    def post(self, request, **kwargs):
        if request.user.is_anonymous():
            return HttpResponseRedirect("/")
        form = AdspotForm(request.POST)
        print request.POST
        if form.is_valid():
            spot=AdSpot.objects.create(name=form.cleaned_data['name'],  site=form.cleaned_data['site'])
            spot.format=form.cleaned_data['format']
            spot.save()
            return HttpResponseRedirect("/platform/sites/%d/" % spot.site.id)
        else:
            return self.render_to_response({"form": form, "format_choice":self.get_format(request), "site_choice":self.get_sites(request)})
#
class AdspotForm(forms.ModelForm):
    class Meta:
        fields = ['name','site','format']
        model = AdSpot
    # name = forms.CharField(max_length=100, required=True,validators=[validate_adspot_name])
    # site = forms.ModelChoiceField(queryset=UserSite.objects.all(), required=True)
    # format = forms.ModelMultipleChoiceField(queryset=AdFormat.objects.all(),required=True)

#


# def get_sites(request):
#     sites = UserSite.objects.filter(user=request.user)
#     return json.dumps(sites)
#
# def get_adspots_by_site(request, pk):
#     site = UserSite.objects.filter(user=request.user, pk=pk)
#     adspots_list = site.adspot_set.all()
#     return json.dumps(adspots_list)
#
#
# def create_site(request, pk):
#     site = UserSite.objects.filter(user=request.user, pk=pk)
#     adspots_list = site.adspot_set.all()
#     return json.dumps(adspots_list)
#
#
