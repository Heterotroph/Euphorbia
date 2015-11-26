# -*- coding: utf-8 -*-

import json
from django import forms
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.core.files.images import get_image_dimensions
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView, FormView
from platform.models import UserSite, AdSpot, AdThematics, AdFormat, Campaign, Banner
from platform.views.sites import LoginRequiredMixin

__author__ = 'igorzygin'

# def validate_adspot_name(value):
#     if len(AdSpot.objects.filter(name=value))>0:
#         raise ValidationError('%s must be unique' % value)
#
# class OneAdspotView(LoginRequiredMixin, TemplateView):
#     template_name = 'adspot_one.html'
#
#     def get_context_data(self, **kwargs):
#         pk=self.kwargs['pk']
#         data = super(OneAdspotView, self).get_context_data(**kwargs)
#         data['adspot'] = AdSpot.objects.get(pk=pk, site__user=self.request.user)
#         print data['adspot']
#         return data

#
#
class CreateBannerView(LoginRequiredMixin, FormView):
    template_name = 'banner_create.html'

    def get_format(self, request):
        return AdFormat.objects.all()

    def get_campaign(self, request):
        return Campaign.objects.filter(user=request.user)


    def get(self, request, **kwargs):
        if request.user.is_anonymous():
            return HttpResponseRedirect("/")
        return self.render_to_response({"form": BannerForm(), "format_choice":self.get_format(request), "campaign_choice":self.get_campaign(request)})

    def post(self, request, **kwargs):
        if request.user.is_anonymous():
            return HttpResponseRedirect("/")
        print request.FILES
        form = BannerForm(request.POST, request.FILES)
        print request.POST
        if form.is_valid():
            banner=Banner.objects.create(url=form.cleaned_data['url'], campaign=form.cleaned_data['campaign'], format=form.cleaned_data['format'], image=form.cleaned_data['image'])
            banner.save()
            return HttpResponseRedirect("/platform/campaigns/%d/" % banner.campaign.id)
        else:
            return self.render_to_response({"form": form, "format_choice":self.get_format(request), "campaign_choice":self.get_campaign(request)})
#
class BannerForm(forms.ModelForm):
    class Meta:
        fields = ['campaign','url','format','image']
        model = Banner


    def clean_image(self):
       image = self.cleaned_data.get("image")
       if not image:
           raise forms.ValidationError("No image!")
       else:

           req_width = 315
           req_height = 300
           if self.cleaned_data["format"].id == 1:
                req_width = 315
                req_height = 300
           elif self.cleaned_data["format"].id == 2:
                req_width = 300
                req_height = 250
           w, h = get_image_dimensions(image)
           if w != req_width:
               raise forms.ValidationError("The image is %i pixel wide. It's supposed to be %i px" % (w, req_width))
           if h != req_height:
               raise forms.ValidationError("The image is %i pixel high. It's supposed to be %i px" % (h, req_height))
       return image
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
