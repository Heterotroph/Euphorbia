import json
from django import forms
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView, FormView
from platform.models import UserSite, AdSpot, AdThematics
from platform.views.other import get_data_from_sql

__author__ = 'igorzygin'


class LoginRequiredMixin(object):
    @classmethod
    def as_view(cls, **initkwargs):
        view = super(LoginRequiredMixin, cls).as_view(**initkwargs)
        return login_required(view)


class SitesView(LoginRequiredMixin, TemplateView):
    template_name = "sites_list.html"

    def get_context_data(self, **kwargs):
        data = super(SitesView, self).get_context_data(**kwargs)
        data['sites_list'] = UserSite.objects.filter(user=self.request.user)
        return data


class OneSiteView(LoginRequiredMixin, TemplateView):
    template_name = 'site_one.html'

    def get_context_data(self, **kwargs):
        pk=self.kwargs['pk']
        data = super(OneSiteView, self).get_context_data(**kwargs)
        data['site'] = UserSite.objects.get(pk=pk, user=self.request.user)
        print data['site']
        return data



class CreateSiteView(LoginRequiredMixin, FormView):
    template_name = 'site_create.html'

    def get_thematics(self):
        return AdThematics.objects.all()


    def get(self, request, **kwargs):
        if request.user.is_anonymous():
            return HttpResponseRedirect("/")
        return self.render_to_response({"form": SiteForm(), "thematics_choice":self.get_thematics()})

    def post(self, request, **kwargs):
        if request.user.is_anonymous():
            return HttpResponseRedirect("/")
        form = SiteForm(request.POST)
        print request.POST
        if form.is_valid():
            site=UserSite.objects.create(user=request.user, name=form.cleaned_data['name'], url=form.cleaned_data['url'])
            site.thematics=form.cleaned_data['thematics']
            site.save()
            return HttpResponseRedirect("/platform/sites/")
        else:
            return self.render_to_response({"form": form, "thematics_choice":self.get_thematics()})



def get_sites(request):
    sites = UserSite.objects.filter(user=request.user)
    return json.dumps(sites)

def get_adspots_by_site(request, pk):
    site = UserSite.objects.filter(user=request.user, pk=pk)
    adspots_list = site.adspot_set.all()
    return json.dumps(adspots_list)


def create_site(request, pk):
    site = UserSite.objects.filter(user=request.user, pk=pk)
    adspots_list = site.adspot_set.all()
    return json.dumps(adspots_list)


class SiteForm(forms.Form):
    name = forms.CharField(max_length=100, required=True)
    url = forms.CharField(max_length=100, required=True)
    thematics = forms.ModelMultipleChoiceField(queryset=AdThematics.objects.all(),required=True)




def get_site_stats(site_id_list):
    site_id_string = ','.join(site_id_list)
    query = 'select pus.id, CURRENT_DATE - s.a AS date, count(DISTINCT bss.id), count(DISTINCT bcc.id) \
            from platform_usersite as pus \
            inner join \
            Generate_series(0, 30, 1) AS s(a) \
            On true \
            LEFT JOIN platform_adspot as pa \
            ON pa.site_id=pus.id \
            LEFT JOIN banner_show_stats as bss \
            ON date(bss.created)=CURRENT_DATE - s.a and bss.spot_code=pa.unique_code \
            LEFT JOIN banner_clicks as bcc \
            On date(bcc.created)=CURRENT_DATE - s.a AND bcc.spot_code=pa.unique_code \
            WHERE pus.id in (%s) \
            GROUP BY pus.id, CURRENT_DATE - s.a' % site_id_string
    data = get_data_from_sql(query)
    return data