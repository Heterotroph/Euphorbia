from platform.models import UserSite, AdSpot
from platform.views.other import get_data_from_sql

__author__ = 'igor'


def get_publisher_stats(request):
    data = []
    sites_list = UserSite.objects.filter(user=request.user)
    site_id_list = [site.id for site in sites_list]
    query = "select pa.site_id as site_id, count(bss) as shows, count(bc) as clicks \
            from platform_adspot as pa \
            left join \
            banner_show_stats as bss \
            on bss.spot_code = pa.unique_code \
            left join  \
            banner_clicks as bc \
            on bc.spot_code = pa.unique_code \
            where pa.site_id in (2) \
            group by pa.site_id;"

    data = get_data_from_sql(query)
    for entry in data:
        for site in sites_list:
            if site.id == entry['site_id']:
                entry['site'] = site
                break
                
    return data