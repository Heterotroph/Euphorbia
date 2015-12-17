from platform.models import UserSite, AdSpot
from platform.views.other import get_data_from_sql

__author__ = 'igor'


def get_publisher_stats(user, from_date, to_date):
    sites_list = UserSite.objects.filter(user=user)
    site_id_list = [site.id for site in sites_list]
    site_id_list_str = ",".join(site_id_list)


    date_diff = (to_date-from_date)/(3600*24)
    query = "select CURRENT_DATE - s.a AS date, pa.site_id as site_id, count(bss) as shows, count(bc) as clicks \
            from Generate_series(%d, 0, -1) AS s(a) \
            inner join  \
            platform_adspot as pa \
            on 1=1 \
            left join  \
            banner_show_stats as bss \
            on bss.spot_code = pa.unique_code and date(bss.created)=CURRENT_DATE - s.a \
            left join  \
            banner_clicks as bc \
            on bc.spot_code = pa.unique_code and date(bss.created)=CURRENT_DATE - s.a \
            where pa.site_id in (%s) \
            group by pa.site_id,CURRENT_DATE - s.a;" % (date_diff, site_id_list_str)

    data = get_data_from_sql(query)
    for entry in data:
        for site in sites_list:
            if site.id == entry['site_id']:
                entry['site'] = site
                break

    return data