# -*- coding: utf-8 -*-
import json
from django.contrib.auth import logout

from django.db import connection


# Create your views here.
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, JsonResponse
from django.template import RequestContext
from platform.models import UserSite, UserPixel
from datetime import timedelta, datetime

def to_unixtime(dt):
    timestamp = (dt - datetime(1970, 1, 1)).total_seconds()
    return int(timestamp)



default_from_days_ago = 29
default_to_days_ago = 0
max_xAxis_len = 40

default_to_date = to_unixtime(datetime.now() - timedelta(days=int(default_to_days_ago)))
default_from_date = to_unixtime(datetime.now() - timedelta(days=int(default_from_days_ago)))
print default_to_date, default_from_date


#
#   -||-||-||-||-||-
#    PLATFORM VIEWS
#   -||-||-||-||-||-
#


#
#   Вход, регистрация и т.п.
#
#   Страница входа, login. => django.contrib.auth.views.login
#


#
#   Страница регистрации
#
def register(request):
    return render_to_response("register.html")


#
#   Выход
#
def logout_view(request):
    logout(request)
    return HttpResponseRedirect("/")

#
#   Страница профиля
#
@login_required
def profile(request):
    return HttpResponseRedirect("/platform/tracking/")


#
#   Обработка данных трекинга
#
#   Страница трекинга.
#
@login_required
def tracking(request):
    # Данные для меню
    left_menu_data = get_menu(request)
    left_menu_links = get_menu_links(request)

    # Данные для тулбара
    toolbar_dates = get_toolbar_dates(request)

    # Данные для таблицы
    treetable_data, sp_id_data = get_sites(request)

    # Данные для графика показов
    views_chart_data = get_views_data(treetable_data[0]["spID"], None, default_to_days_ago, default_from_days_ago) if len(treetable_data)>0 else []
    #views_chart_axis_steps = get_views_steps(views_chart_data, ["views", "reqs"])

    # Данные для графика времени посещений
    time_chart_data = get_time_data(treetable_data[0]["spID"], None, default_to_days_ago, default_from_days_ago) if len(treetable_data)>0 else []
    #time_chart_axis_steps = get_views_steps(time_chart_data, ["active", "total"])


    left_menu_data = json.dumps(left_menu_data)
    left_menu_links = json.dumps(left_menu_links)
    toolbar_dates = json.dumps(toolbar_dates)
    treetable_data = json.dumps(treetable_data)
    views_chart_data = json.dumps(views_chart_data)
    #views_chart_axis_steps = json.dumps(views_chart_axis_steps)
    time_chart_data = json.dumps(time_chart_data)
    #time_chart_axis_steps = json.dumps(time_chart_axis_steps)

    context = {
        "left_menu_data": left_menu_data,
        "left_menu_links": left_menu_links,
        "toolbar_dates": toolbar_dates,
        "treetable_data": treetable_data,
        "sp_id_data": sp_id_data,
        #"views_chart_axis_steps": views_chart_axis_steps,
        #"time_chart_axis_steps": time_chart_axis_steps,
        "views_chart_data": views_chart_data,
        "time_chart_data": time_chart_data,
        "to_date": default_to_date,
        "from_date": default_from_date
        }
    return render_to_response("tracking.html", context, context_instance=RequestContext(request))


#
#   Обработка AJAX приходящих с tracking.
#
def tracking_ajax(request):
    command = request.GET.get("command")
    return JsonResponse(get_command(command)(request))

def get_command(com):
    return {
        "get_data_by_sp_id": get_site_data,
        "get_refresh_data": get_refresh_data
    }.get(com)

#
#   Получить данные выбранного сайта/страницы (AJAX)
#
def get_site_data(request):

    # Данные для графика показов
    views_chart_data = get_views_data_request(request)
    #views_chart_axis_steps = get_views_steps(views_chart_data, ["views", "reqs"])

    # Данные для графика времени посещений
    time_chart_data = get_time_data_request(request)
    #time_chart_axis_steps = get_views_steps(time_chart_data, ["active", "total"])

    sp_name = get_sp_name(request)

    result = {
        "visitChartData": views_chart_data,
        #"visitChartYAxis": views_chart_axis_steps,
        "timeChartData": time_chart_data,
        #"timeChartYAxis": time_chart_axis_steps,
        "spName": sp_name
    }

    return result

#
#   Обработка "обновить" (AJAX)
#
def get_refresh_data(request):

    views_time_data = get_site_data(request)
    treetable_data, sp_id_data = get_sites(request)

    views_time_data["trackTreetableData"] = treetable_data
    views_time_data["spIDData"] = sp_id_data
    views_time_data["toolbarDates"] = get_toolbar_dates(request)

    return views_time_data


#
#   Формирование списка для выбора дат
#
def get_toolbar_dates(request):
    return ["Сегодня", "Вчера", "Октябрь", "Сентябрь"]


#
#   Получение списка сайтов и пикселей для treetable
#   Ёбнутая архитектура у метода получилась. Просто пиздец. Его бы разбить на 3 - 4...
#
def get_sites(request):
    sites_list = UserSite.objects.filter(user=request.user)

    result_data = []
    sp_data_map = {}

    data = []
    site_counter = 1
    is_open = True

    for site in sites_list:
        pixel_list = site.userpixel_set.all()
        pixels_data = []

        if len(pixel_list) != 0:
            pixel_map = {pixel.unique_code: pixel for pixel in pixel_list}
            pixel_code_list = [pixel.unique_code for pixel in pixel_list]
            pixel_code_list_str = "'%s'" % ("', '".join(pixel_code_list))
            from_date = int(request.GET["from_date"]) if "from_date" in request.GET else default_from_date
            to_date = int(request.GET["to_date"]) if "to_date" in request.GET else default_to_date


            query = "\
                SELECT page_unique_code,                                                                   \
                       Median(Coalesce(active_time, 0))                                                    \
                       AS active,                                                                          \
                       Median(EXTRACT(epoch FROM (Coalesce(session_updated, created) - created))) AS total,\
                       COUNT(session_id) AS visits,                                                        \
                       COUNT(DISTINCT local_user_id) AS unique_visits                                      \
                FROM   page_sessions_link                                                                  \
                WHERE  os != 'NULL'                                                                        \
                       AND browser != 'NULL'                                                               \
                       AND page_unique_code IN ( %s )                                                      \
                       AND created >= to_timestamp(%s)  AT TIME ZONE 'UTC'                                                               \
                       AND created <= to_timestamp(%s)  AT TIME ZONE 'UTC'                                                              \
                GROUP  BY page_unique_code                                                                 \
                ORDER  BY page_unique_code " % (pixel_code_list_str, str(from_date), str(to_date))
            print(query)
            data = get_data_from_sql(query)

            pixel_counter = 1

            is_open = len(data)
            if (is_open):
                for entry in data:
                    pixel = pixel_map[entry["page_unique_code"]]
                    del pixel_map[entry["page_unique_code"]]
                    pixel_entry = {"id": str(site_counter) + "." + str(pixel_counter),
                                   "value": pixel.name + " (" + pixel.unique_code + ")", "time": time_presentation(entry["total"], " сек."),
                                   "active": time_presentation(entry["active"], " сек."),
                                   "visits": entry["visits"], "uniq": entry["unique_visits"], "spID": pixel.id}
                    pixels_data.append(pixel_entry)
                    sp_data_map[str(site_counter) + "." + str(pixel_counter)] = pixel.id;
                    pixel_counter += 1
                for entry in pixel_map:
                    pixel = pixel_map[entry]
                    pixel_entry = {"id": str(site_counter) + "." + str(pixel_counter),
                                   "value": pixel.name + " (" + pixel.unique_code + ")", "time": "0 сек.",
                                   "active": "0 сек.", "visits": 0, "uniq": 0, "spID": pixel.id}
                    pixels_data.append(pixel_entry)
                    sp_data_map[str(site_counter) + "." + str(pixel_counter)] = pixel.id;
                    pixel_counter += 1
            else:
                for entry in pixel_list:
                    pixel = entry
                    pixel_entry = {"id": str(site_counter) + "." + str(pixel_counter),
                                   "value": pixel.name + " (" + pixel.unique_code + ")", "time": "0 сек.",
                                   "active": "0 сек.", "visits": 0, "uniq": 0, "spID": pixel.id}
                    pixels_data.append(pixel_entry)
                    sp_data_map[str(site_counter) + "." + str(pixel_counter)] = pixel.id;
                    pixel_counter += 1

            site_active = time_presentation(sum([entry["active"] for entry in data]) / len(data) if len(data) > 0 else 0, " сек.")
            site_time = time_presentation(sum([entry["total"] for entry in data]) / len(data) if len(data) > 0 else 0, " сек.")
            site_visits = sum([entry["visits"] for entry in data])
            site_unique_visits = sum([entry["unique_visits"] for entry in data])
        else:
            site_active = "0 сек."
            site_time = "0 сек."
            site_visits = 0
            site_unique_visits = 0

        site_data = {"id": str(site_counter), "value": site.name, "time": site_time, "active": site_active,
                     "visits": site_visits, "uniq": site_unique_visits, "open": is_open, "data": pixels_data,
                     "spID": site.id}
        result_data.append(site_data)
        sp_data_map[str(site_counter)] = site.id;
        site_counter += 1
    #result_data.sort(key=lambda obj: obj["visits"], reverse=True)
    return result_data, sp_data_map


#
#   Имя сайта-пикселя по данным из запроса
#
def get_sp_name(request):
    site_id = request.GET["site_id"] if "site_id" in request.GET else None
    page_id = request.GET["page_id"] if "page_id" in request.GET else None
    if site_id is not None:
        return UserSite.objects.get(pk=site_id).name
    else:
        return UserPixel.objects.get(pk=page_id).name

#
#   Получение данных показов (request)
#
def get_views_data_request(request):
    site_id = request.GET["site_id"] if "site_id" in request.GET else None
    page_id = request.GET["page_id"] if "page_id" in request.GET else None
    from_date = int(request.GET["from_date"]) if "from_date" in request.GET else default_from_date
    to_date = int(request.GET["to_date"]) if "to_date" in request.GET else default_to_date
    return get_views_data(site_id, page_id, from_date, to_date)

#
#   Получение данных показов (site_id, page_id, to_days_ago, from_days_ago)
#
def get_views_data(site_id, page_id, from_date, to_date):
    result_data = []
    pixel_code_list = []
    if site_id is not None:
        site = UserSite.objects.get(pk=site_id)
        pixel_list = site.userpixel_set.all()
        pixel_code_list = [pixel.unique_code for pixel in pixel_list]
    else:
        pixel = UserPixel.objects.get(pk=page_id)
        pixel_code_list = [pixel.unique_code]

    date_diff = (to_date-from_date)/(3600*24)

    pixel_code_list_str = "'%s'" % ("', '".join(pixel_code_list))
    query = "\
        SELECT    to_timestamp(%s)::date - s.a         AS date,                                     \
                  COALESCE(visits, 0)        AS visits,                                   \
                  COALESCE(unique_visits, 0) AS unique_visits                             \
        FROM      Generate_series(%s, 0, -1) AS s(a)                                     \
        LEFT JOIN                                                                         \
                  (                                                                       \
                           SELECT   Date(created)                 AS date,                \
                                    Count(session_id)             AS visits,              \
                                    Count(DISTINCT local_user_id) AS unique_visits        \
                           FROM     page_sessions_link                                    \
                           WHERE    os != 'NULL'                                          \
                                    AND      browser != 'NULL'                            \
                                    AND      page_unique_code IN ( %s )                   \
                           GROUP BY date(created)                                         \
                           ORDER BY date(created)) AS data_table                          \
        ON        CURRENT_DATE - s.a = data_table.date;" % (str(to_date),date_diff, pixel_code_list_str)
    print query
    data = get_data_from_sql(query)

    counter = 0
    print(len(data))
    for entry in data:
        #result_data.append({"id": counter, "views": entry["visits"], "reqs": entry["unique_visits"], "xAxis": str(entry["date"])})
        axis_cond = len(data) < max_xAxis_len or counter % 2 == 0
        result_data.append({"id": counter, "views": entry["visits"], "reqs": entry["unique_visits"], "xAxis": str(entry["date"]).split("-")[2] if axis_cond else ""})
        counter += 1
    # return [{"views": entry["visits"], "reqs": entry["unique_visits"], "xAxis": idx} for idx, entry in data]
    return result_data


#
#   Получение данных времени (request)
#
def get_time_data_request(request):
    site_id = request.GET["site_id"] if "site_id" in request.GET else None
    page_id = request.GET["page_id"] if "page_id" in request.GET else None
    from_date = int(request.GET["from_date"]) if "from_date" in request.GET else default_from_date
    to_date = int(request.GET["to_date"]) if "to_date" in request.GET else default_to_date
    return get_time_data(site_id, page_id, from_date, to_date)

#
#   Получение данных времени (site_id, page_id, to_days_ago, from_days_ago)
#
def get_time_data(site_id, page_id, from_date, to_date):
    result_data = []
    pixel_code_list = []
    if site_id is not None:
        site = UserSite.objects.get(pk=site_id)
        pixel_list = site.userpixel_set.all()
        pixel_code_list = [pixel.unique_code for pixel in pixel_list]
    else:
        pixel = UserPixel.objects.get(pk=page_id)
        pixel_code_list = [pixel.unique_code]
    pixel_code_list_str = "'%s'" % ("', '".join(pixel_code_list))

    date_diff = (to_date-from_date)/(3600*24)

    query = "\
        SELECT    to_timestamp(%s)::date - s.a   AS date,                                                                                                                               \
                  COALESCE(active, 0)        AS active,                                                                                                                             \
                  COALESCE(total, 0)         AS total                                                                                                                               \
        FROM      Generate_series(%s, 0, -1) AS s(a)                                                                                                                               \
        LEFT JOIN                                                                                                                                                                   \
                  (                                                                                                                                                                 \
                           SELECT   Date(created)                                                                                                           AS date,                \
                                    Median(COALESCE(active_time, 0))                                                                                        AS active,              \
                                    Greatest(Median(Extract(epoch FROM ( COALESCE(session_updated, created) - created))), Median(COALESCE(active_time, 0))) AS total                \
                           FROM     page_sessions_link                                                                                                                              \
                           WHERE    os != 'NULL'                                                                                                                                    \
                                    AND      browser != 'NULL'                                                                                                                      \
                                    AND      page_unique_code IN ( %s )                                                                                                             \
                           GROUP BY date(created)                                                                                                                                   \
                           ORDER BY date(created)) AS data_table                                                                                                                    \
        ON        CURRENT_DATE - s.a = data_table.date;" % (str(to_date), str(date_diff), pixel_code_list_str)
    data = get_data_from_sql(query)

    counter = 0
    for entry in data:
        #result_data.append({"active": entry["active"], "total": entry["total"], "xAxis": str(entry["date"])})
        axis_cond = len(data) < max_xAxis_len or counter % 2 == 0
        result_data.append({"id": counter, "active": int(entry["active"]), "total": int(entry["total"]), "xAxis": str(entry["date"]).split("-")[2] if axis_cond else ""})
        counter += 1
    # return [{"active": entry["active"], "total": entry["total"], "xAxis": idx} for idx, entry in data]
    return result_data


#
#   Формирование настроек для графика относительно данных
#
def get_views_steps(data, key_list):
    max_value = max([max([entry[key] for entry in data]) for key in key_list]) if len(data) > 0 else 10
    max_value = 10 if max_value < 10 else max_value
    max_value = max_value * 1.2
    step = max_value / 10
    return {"start": 0,
            "step": int(step),
            "end": int(max_value)}


#
#   Получение элементов меню (Необходимо формировать универсально, относительно пользователя)
#
def get_menu(request):
    arr = [
        {
            "id": "1",
            "value": "Трекинг",
            "icon": "sitemap"
        }, {
            "id": "2",
            "value": "Платформы",
            "icon": "server"
        }, {
            "id": "3",
            "value": "Реклама",
            "icon": "list-alt"
        }, {
            "id": "4",
            "value": "Профиль",
            "icon": "user"
        }, {
            "id": "5",
            "value": "Выход",
            "icon": "sign-out"
        }
    ]
    return arr

#
#   Получение ссылок меню
#
def get_menu_links(request):
    arr = ["/platform/tracking/",
           "/platform/sites/",
           "/platform/advert/",
           "/platform/profile/",
           "/platform/logout"]
    return arr



#
#   -||-||-||-||-||-
#         UTILS
#   -||-||-||-||-||-
#


def get_data_from_sql(query):
    cursor = connection.cursor()
    cursor.execute(query)
    data = dictfetchall(cursor)
    return data

def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
        ]

#
#   Форматирование секунд
#
def to_hms(seconds):
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    return "%02d:%02d:%02d" % (h, m, s)

#
#   Форматирование секунд (РАСШИРЕННОЕ)
#
def time_presentation(seconds, prefix0="", prefix1=""):
    if seconds < 60:
        return "{:2.0f}".format(seconds) + prefix0
    else:
        return to_hms(seconds) + prefix1


