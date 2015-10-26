# -*- coding: utf-8 -*-
import json

from django.db import connection
from django.shortcuts import render


# Create your views here.
from adboxweb.forms import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.core.context_processors import csrf

from adboxweb.models import Banner, BannerRequest, CampaignRequest
from django.views.generic.base import TemplateResponse, RedirectView
from rotator.models import UserSite, UserPixel


@csrf_protect
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password1'],
            email=form.cleaned_data['email']
            )
            from django.contrib.auth.models import Group
            g = Group.objects.get(name='publisher')
            g.user_set.add(user)
            return HttpResponseRedirect('/register/success/')
    else:
        form = RegistrationForm()
    variables = RequestContext(request, {
    'form': form
    })

    return render_to_response(
    'registration/register.html',
    variables,
    )

def register_success(request):
    return render_to_response(
    'registration/success.html',
    )

def logout_page(request):
    logout(request)
    return HttpResponseRedirect('/')

def index(request):
    return render_to_response(
    'index.html',
    )


@login_required
def home(request):
    banner_list=Banner.objects.all()
    is_publisher=True
    is_advertiser=True
    return render_to_response(
    'home.html',
    { 'user': request.user, 'banner_list':banner_list, 'is_publisher':is_publisher,'is_advertiser':is_advertiser }
    )

def thanks(request):
    return render_to_response(
    'thanks.html',
    { 'user': request.user,}
    )

def faq(request):
    return render_to_response(
    'faq.html',
    { 'user': request.user,}
    )
def instructions(request):
    return render_to_response(
    'instructions.html',
    { 'user': request.user,}
    )
def conditions(request):
    return render_to_response(
    'conditions.html',
    { 'user': request.user,}
    )
def formats(request):
    return render_to_response(
    'formats.html',
    { 'user': request.user,}
    )

@login_required
def new_banner(request):
    if request.method == 'POST': # If the form has been submitted...
        form = BannerForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            adriver_id = form.cleaned_data['adriver_id']
            url_snippet = form.cleaned_data['url_snippet']
            banner=Banner.objects.create(adriver_id=adriver_id,url_snippet=url_snippet,user=User.objects.all()[0])
            saved=banner.save()
            if saved:
                return HttpResponseRedirect('/home/') # Redirect after POST
            else:
                return HttpResponseRedirect('/home/') # Redirect after PO
    else:
        form = BannerForm() # An unbound form
    mdict = {'form':form, }
    mdict.update(csrf(request))
    return render_to_response('banner_form.html', mdict)

"""@login_required
def banner_list(request):
    import datetime
    from datetime import date

    try:
        date_from=request.GET.get('start',date(2002, 12, 4).isoformat())
        date_to=request.GET.get('end',date.today().isoformat())
        d = datetime.datetime.strptime(date_from, "%Y-%m-%d" )
        d = datetime.datetime.strptime(date_to, "%Y-%m-%d" )
    except ValueError:
        date_from=date(2002, 12, 4).isoformat()
        date_to=date.today().isoformat()
    site_list=Site.objects.all()
    rendered_banner_data=[]

    for site in site_list:
        sum_of_banner={'clicks':0,'views':0,'money_spent':0}
        one_campaign_list={'id':site.id,'name':site.name,'sum_of_banner':sum_of_banner}
        banner_array=site.banner_set.all()
        one_campaign_list['site_set']=[]
        for banner in banner_array:
            import adriver
            clicks, views = adriver.get_slice_clicks_and_views(banner.adriver_id, start=date_from, stop=date_to)
            money_spent = clicks
            one_campaign_list['site_set'].append({'id': banner.id, 'name': banner.name, 'clicks': clicks, 'views': views, 'ctr': 0 if views==0 else float(clicks)/views})
            sum_of_banner['clicks'] += clicks
            sum_of_banner['views'] += views
        sum_of_banner['ctr'] = 0 if sum_of_banner['views']==0 else float(sum_of_banner['clicks'])/sum_of_banner['views']
        # sum_of_banner['money_left'] = sum_of_banner['ctr']
        rendered_banner_data.append(one_campaign_list)
    print rendered_banner_data
    return render_to_response(
    'banners.html',
    {'user': request.user, 'banner_list_array': rendered_banner_data, 'date_from': date_from, 'date_to': date_to}
    )"""








@login_required
def publisher(request):
    left_menu_data = get_menu(request)
    left_menu_links = get_menu_links(request)
    toolbar_dates = get_toolbar_dates(request)
    treetable_data = get_sites(request)
    views_chart_data = get_views_data(request, """ первый айди в treetable_data """)
    views_chart_axis_steps = get_views_steps(views_chart_data, ["views","reqs"])
    time_chart_data = get_time_data(request, """ первый айди в treetable_data """)
    time_chart_axis_steps = time_chart_data(time_chart_data, ["active","total"])
    context= {'left_menu_data':left_menu_data, 'left_menu_links':left_menu_links, 'toolbar_dates':toolbar_dates, 'treetable_data':treetable_data, 'views_chart_data':views_chart_data, 'views_chart_axis_steps':views_chart_axis_steps, 'time_chart_data':time_chart_data, 'time_chart_axis_steps':time_chart_axis_steps}
    return render_to_response("publisher.html", context, context_instance=RequestContext(request))


def get_menu(request):
    arr = [{"id": "1",
        "value": "Трекинг",
        "icon": "sitemap"
        }, {
           "id": "2",
           "value": "Реклама",
           "icon": "list-alt"
       }, {
           "id": "3",
           "value": "Профиль",
           "icon": "user"
       }, {
           "id": "4",
           "value": "Выход",
           "icon": "sign-out"
       }]
    return arr


def get_menu_links(request):
    arr = ["javascript:alert(\"Трекинг\")",
            "javascript:alert(\"Реклама\")",
            "/accounts/profile/",
            "/logout"]
    return arr

def get_toolbar_dates(request):
    return ["Сегодня", "Вчера", "Октябрь", "Сентябрь"]

def get_sites(request):
    sites_list = UserSite.objects.filter(user = request.user)
    data=[]
    for site in sites_list:
        pixel_list = site.userpixel_set.all()
        pixel_map = {pixel.unique_code: pixel for pixel in pixel_list}
        pixel_code_list = [pixel.unique_code for pixel in pixel_list]
        pixel_code_list_str = "'%s'" % ("', '".join(pixel_code_list))
        query = "SELECT page_unique_code, median(active_time) as active, median(EXTRACT(EPOCH FROM (session_updated-created))) AS total, count(session_id) as visits, count(local_user_id) as unique_visits \
                    FROM page_sessions_link \
                    WHERE active_time IS NOT NULL AND page_unique_code in (%s) \
                    GROUP BY page_unique_code \
                    ORDER BY page_unique_code" % pixel_code_list_str
        data = get_data_from_sql(query)
        pixels_data = []
        for entry in data:
            pixel = pixel_map[data['page_unique_code']]
            pixel_entry = {"id":pixel.id, "value":pixel.name, "time":entry['total'], "active":entry['active'], "visits":entry['visits'], "uniq":entry['unique_visits']}
            pixels_data.append(pixel_entry)
        site_active = sum([entry['active'] for entry in data])/len(data)
        site_time = sum([entry['total'] for entry in data])/len(data)
        site_visits = sum([entry['visits'] for entry in data])/len(data)
        site_unique_visits = sum([entry['unique_visits'] for entry in data])/len(data)
        site_data = {"id":site.id, "value":site.name, "time":site_time, "active":site_active,
                     "visits":site_visits, "uniq":site_unique_visits, "open":True, "data":pixels_data}
        data.append(site_data)
    return data


def get_views_data(request):
    site_id = request.GET['site_id'] if 'site_id' in request.GET else None
    page_id = request.GET['page_id'] if 'page_id' in request.GET else None
    pixel_code_list = []
    if site_id is not None:
        site = UserSite.objects.get(pk=site_id)
        pixel_list = site.userpixel_set.all()
        pixel_code_list = [pixel.unique_code for pixel in pixel_list]
    else:
        pixel = UserPixel.objects.get(pk=page_id)
        pixel_code_list = [pixel.unique_code]
    pixel_code_list_str = "'%s'" % ("', '".join(pixel_code_list))
    query = "SELECT date(created) as date, count(session_id) as visits, count(local_user_id) as unique_visits \
                    FROM page_sessions_link \
                    WHERE page_unique_code in (%s) \
                    GROUP BY date(created) \
                    ORDER BY date(created)" % pixel_code_list_str
    data = get_data_from_sql(query)
    return [{"views":entry['visits'], "reqs":entry['unique_visits'], "xAxis":idx} for idx, entry in data]

def get_time_data(request):
    site_id = request.GET['site_id'] if 'site_id' in request.GET else None
    page_id = request.GET['page_id'] if 'page_id' in request.GET else None
    pixel_code_list = []
    if site_id is not None:
        site = UserSite.objects.get(pk=site_id)
        pixel_list = site.userpixel_set.all()
        pixel_code_list = [pixel.unique_code for pixel in pixel_list]
    else:
        pixel = UserPixel.objects.get(pk=page_id)
        pixel_code_list = [pixel.unique_code]
    pixel_code_list_str = "'%s'" % ("', '".join(pixel_code_list))
    query = "SELECT date(created) as date, median(active_time) as active, median(EXTRACT(EPOCH FROM (session_updated-created))) as total \
                    FROM page_sessions_link \
                    WHERE page_unique_code in (%s) \
                    GROUP BY date(created) \
                    ORDER BY date(created)" % pixel_code_list_str
    data = get_data_from_sql(query)
    return [{"active":entry['active'], "total":entry['total'], "xAxis":idx} for idx, entry in data]

def get_views_steps(data, key_list):
    max = max([max([entry[key] for entry in data]) for key in key_list])
    max = max * 1.1
    step = max/10
    return {"start":0,
            "step":int(step),
            "end":int(max)}


def get_data_from_sql(query):
    cursor = connection.cursor()
    cursor.execute(query)
    data = dictfetchall(cursor)
    return data


def publisher_ajax(request):
    command = request.GET.get("command")
    return HttpResponse(get_command(command)(request))

def get_command(com):
    return {
        'set_date': refresh_data,
        'refresh': refresh_data,
        'create_site': create_site,
        'create_tracking': create_tracking,
        'edit_site': edit_site,
        'select_site': select_site,
        }.get(com)

def refresh_data(request):
    toolbar_dates = get_toolbar_dates(request.user)
    treetable_data = get_sites(request.user)
    views_chart_data = get_views_data(request.user, """ первый айди в treetable_data """)
    views_chart_axis_steps = get_views_steps(request.user)
    time_chart_data = get_time_data(request.user, """ первый айди в treetable_data """)
    time_chart_axis_steps = get_time_steps(request.user)
    #из этого собрать любой большой JSON. Я разберусь
    return HttpResponse("Данные таблиц и графиков");











def example(pixel_id):
    cursor = connection.cursor()
    pixel = UserPixel.objects.get(pk=1)
    cursor.execute("SELECT pixel_id, count(*) FROM pixel_loads WHERE pixel_id = %s GROUP BY pixel_id", pixel.unique_code)
    pixel_stats = dictfetchall(cursor)
    return HttpResponse("return this string")

def example2(arg):
    cursor = connection.cursor()
    cursor.execute("SELECT median(active_time) as active, date(created), median(EXTRACT(EPOCH FROM (session_updated-created))) as total from page_sessions_link where active_time is not null and page_unique_code='F27A96423901455' group by date(created)")
    test_data = dictfetchall(cursor)
    for data1 in test_data:
        data1['date']=data1['date'].strftime('%d.%m.%Y')
    return HttpResponse(test_data)

def example3(request):
    sites_list = list(UserSite.objects.filter(user=request.user))
    pixel_list = list(UserPixel.objects.filter(site__in=sites_list))
    pixel_code_list = [pixel.unique_code for pixel in pixel_list]
    pixel_map = {pixel.unique_code: pixel for pixel in pixel_list}

    pixel_code_list_string = "'"+"','".join(pixel_code_list)+"'"

    query = "select date(created) as date, count(session_id), count(local_user_id), page_unique_code from \
    page_sessions_link where page_unique_code in (%s) group by date(created), page_unique_code;" % pixel_code_list_string
    cursor = connection.cursor()
    cursor.execute(query)
    data = dictfetchall(cursor)
    for entry in data:
        page_unique_code = entry.pop('page_unique_code')
        page = pixel_map[page_unique_code]
        site = page.site
        entry['site']={"id":site.id,"site_name":site.name}
        entry['page']={"id":page.id,"page_name":page.name}
        entry['date']=entry['date'].strftime('%d.%m.%Y')
    return HttpResponse(json.dumps(data))

def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
        ]

@login_required
def campaign_list(request):
    import datetime
    from datetime import date

    try:
        date_from=request.GET.get('start',date(2002, 12, 4).isoformat())
        date_to=request.GET.get('end',date.today().isoformat())
        d = datetime.datetime.strptime(date_from, "%Y-%m-%d" )
        d = datetime.datetime.strptime(date_to, "%Y-%m-%d" )
    except ValueError:
        date_from=date(2002, 12, 4).isoformat()
        date_to=date.today().isoformat()
    from adboxweb.models import CampaignList
    campaign_list_array=CampaignList.objects.all()
    rendered_campaign_data=[]

    for campaign_list in campaign_list_array:
        sum_of_campains={'clicks':0,'views':0,'ctr':0}
        one_campaign_list={'id':campaign_list.id,'name':campaign_list.name,'sum_of_campains':sum_of_campains}
        campaign_array=campaign_list.campaign_set.all()
        one_campaign_list['campaign_set']=[]
        for campaign in campaign_array:
            import adriver
            clicks,views,reach = adriver.get_advert_clicks_and_views(campaign.adriver_id, start=date_from, stop=date_to)
            ctr= -1 if views==0 else float(clicks)/views
            print(ctr)
            print(clicks/views)
            money_left=100
            one_campaign_list['campaign_set'].append({'id':campaign.id,'name':campaign.name,'clicks':clicks,'views':views,'ctr':ctr, 'reach':reach})
            sum_of_campains['clicks']+=clicks
            sum_of_campains['views']+=views
        sum_of_campains['ctr']=-1 if sum_of_campains['views']==0 else float(sum_of_campains['clicks'])/sum_of_campains['views']
        rendered_campaign_data.append(one_campaign_list)
    print rendered_campaign_data
    return render_to_response(
    'campaigns.html',
    {'user': request.user, 'campaign_list_array': rendered_campaign_data, 'date_from': date_from, 'date_to': date_to}
    )

@login_required
def edit_banner(request):
    instance = Banner.objects.get(id=id)
    form = BannerForm(request.POST or None, instance=instance)
    if form.is_valid():
          form.save()
          return RedirectView('next_view')
    return TemplateResponse(request, 'banner_form.html', {'form': form})

def register_advertizer(request):
    return render_to_response('registration/register_advertizer.html')

def register_publisher(request):
    if request.method == 'GET':
        return render_to_response('registration/register_publisher.html')
    elif request.method == 'POST':
        return render_to_response('base.html')


def new_banner(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = BannerForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            banner_request = BannerRequest.objects.create(site_url=form.cleaned_data['site_url'], banner_format=form.cleaned_data['banner_format'])
            banner_request.save()
            # redirect to a new URL:
            return HttpResponseRedirect('/thanks/')
    # if a GET (or any other method) we'll create a blank form
    else:
        form = BannerForm()
    return render(request, 'banner_form.html', {'form': form})



def new_campaign(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = CampaignForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            campaign_request = CampaignRequest.objects.create(campaign_name=form.cleaned_data['campaign_name'], campaign_text=form.cleaned_data['campaign_text'])
            campaign_request.save()
            # redirect to a new URL:
            return HttpResponseRedirect('/thanks/')
    # if a GET (or any other method) we'll create a blank form
    else:
        form = CampaignForm()

    return render(request, 'campaign_form.html', {'form': form})