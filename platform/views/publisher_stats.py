from platform.models import UserSite, AdSpot
from platform.views.other import get_data_from_sql
from other import get_menu, get_menu_links, default_from_date, default_to_date
from django.shortcuts import render_to_response
from django.template import RequestContext
import json

__author__ = 'igor'




def test_view(request):
    from_date = int(request.GET["from_date"]) if "from_date" in request.GET else default_from_date
    to_date = int(request.GET["to_date"]) if "to_date" in request.GET else default_to_date
    treatable_data = get_publisher_stats(request.user,from_date, to_date)
    print(treatable_data)

    context = {
        "left_menu_data": get_menu(request),
        "left_menu_links": get_menu_links(request),
        "treetable_data": json.dumps(treatable_data),
        "to_date": to_date,
        "from_date": from_date
        }
    return render_to_response("publisher.html", context, context_instance=RequestContext(request))

def get_publisher_stats(user, from_date, to_date):
    sites_list = UserSite.objects.filter(user=user)
    site_id_list = [str(site.id) for site in sites_list]
    site_id_list_str = ",".join(site_id_list)


    date_diff = (to_date-from_date)/(3600*24)
    query = "select dt.date, pa.site_id as site_id, pa.id as spot_id, count(bss) as shows, count(bc) as clicks from\
            (select to_timestamp(%d)::date - s.a AS date from Generate_series(%d, 0, -1) AS s(a)) as dt\
            inner join \
            platform_adspot as pa                                                                 \
            on 1=1                                                                                 \
            left join                                                                              \
            banner_show_stats as bss                                                               \
            on bss.spot_code = pa.unique_code and date(bss.created)=dt.date                        \
            left join                                                                              \
            banner_clicks as bc                                                                    \
            on bc.spot_code = pa.unique_code and date(bss.created)=dt.date                         \
            where pa.site_id in (%s)                                                                \
            group by pa.id,dt.date;" % (to_date, date_diff, site_id_list_str)

    data = get_data_from_sql(query)
    for entry in data:
        for site in sites_list:
            if site.id == entry['site_id']:
                entry["date"] = str(entry["date"])
                entry['site_name'] = site.name
                break

    return data