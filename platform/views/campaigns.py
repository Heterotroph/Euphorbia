import json
from django import forms
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView, FormView, ListView
from platform.models import UserSite, AdSpot, AdThematics, Campaign
from platform.views.sites import LoginRequiredMixin

__author__ = 'igorzygin'




class CampaignsView(LoginRequiredMixin, ListView):
    template_name = "campaigns_list.html"
    context_object_name = 'campaigns_list'

    def get_queryset(self):
        return Campaign.objects.filter(user=self.request.user)

# `
class OneCampaignView(LoginRequiredMixin, TemplateView):
    template_name = 'campaign_one.html'

    def get_context_data(self, **kwargs):
        pk=self.kwargs['pk']
        data = super(OneCampaignView, self).get_context_data(**kwargs)
        data['campaign'] = Campaign.objects.get(pk=pk, user=self.request.user)
        return data
#
#
#
class CreateCampaignView(LoginRequiredMixin, FormView):
    template_name = 'campaign_create.html'


    def get_thematics(self):
        return AdThematics.objects.all()


    def get(self, request, **kwargs):
        if request.user.is_anonymous():
            return HttpResponseRedirect("/")
        return self.render_to_response({"form": CampaignForm(), "thematics_choice":self.get_thematics()})

    def post(self, request, **kwargs):
        if request.user.is_anonymous():
            return HttpResponseRedirect("/")
        form = CampaignForm(request.POST)
        print request.POST
        if form.is_valid():
            campaign=Campaign.objects.create(user=request.user, name=form.cleaned_data['name'])
            campaign.thematics=form.cleaned_data['thematics']
            campaign.save()
            return HttpResponseRedirect("/platform/campaigns/")
        else:
            return self.render_to_response({"form": form, "thematics_choice":self.get_thematics()})

class CampaignForm(forms.ModelForm):
     class Meta:
        fields = ['name', 'thematics']
        model = Campaign


#
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
