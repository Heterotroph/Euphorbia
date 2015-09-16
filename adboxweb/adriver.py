__author__ = 'igor'

def get_stats(root,tag):
    res=0
    for child in root:
        if child.tag==tag:
            try:
                res+=int(child.text)
            except ValueError:
                res+=0
        res+=get_stats(child,tag)
    return res

def get_text(root,tag):
    res=0
    for child in root:
        print child.tag
        if child.tag==tag:
            return child.text
    return None



def get_slice_clicks_and_views(avd_id,start, stop):
    import urllib2
    url='https://api.adriver.ru/login'
    headers = { 'X-Auth-Login': 'adriver_kaz',
                'X-Auth-Passwd': 'adriverimg'}
    req = urllib2.Request(url, headers=headers)
    response = urllib2.urlopen(req)
    the_page = response.read()
    import xml.etree.ElementTree as ET
    tree = ET.fromstring(the_page)
    root = tree
    userId=get_text(root,'userId')
    token=get_text(root,'token')
    url='https://api.adriver.ru/stat/slices/'+str(avd_id)+'?start_date='+start+'&stop_date='+stop+'&granularity=daily'
    print url
    headers = { 'X-Auth-userId': userId,
                'X-Auth-Passwd': token}
    print headers
    #data = urllib.urlencode(values)
    req = urllib2.Request(url, headers=headers)
    response = urllib2.urlopen(req)
    the_page = response.read()
    import xml.etree.ElementTree as ET
    tree = ET.fromstring(the_page)
    root = tree
    # for child in root:
    #     print child.tag
    #     if child.tag==u'{http://www.w3.org/2005/Atom}content':
    #         child = child[0]
    #         for child_child in child:
    #             print child_child
    #             if child_child.tag==u'{http://adriver.ru/ns/restapi/atom}stat':
    #                  for child_child_child in child_child:
    #                     print child_child_child
    clicks=get_stats(root,'{http://adriver.ru/ns/restapi/atom}click')
    views=get_stats(root,'{http://adriver.ru/ns/restapi/atom}exp')
    return clicks, views

def get_advert_clicks_and_views(avd_id,start, stop):
    import urllib2
    reach = 0
    url='https://api.adriver.ru/login'
    headers = { 'X-Auth-Login': 'adriver_kaz',
                'X-Auth-Passwd': 'adriverimg'}
    req = urllib2.Request(url, headers=headers)
    response = urllib2.urlopen(req)
    the_page = response.read()
    import xml.etree.ElementTree as ET
    tree = ET.fromstring(the_page)
    root = tree
    userId=get_text(root,'userId')
    token=get_text(root,'token')
    url='https://api.adriver.ru/stat/ads/'+str(avd_id)+'?start_date='+start+'&stop_date='+stop+'&granularity=daily'
    print url
    headers = { 'X-Auth-userId': userId,
                'X-Auth-Passwd': token}
    #data = urllib.urlencode(values)
    req = urllib2.Request(url, headers=headers)
    response = urllib2.urlopen(req)
    the_page = response.read()
    import xml.etree.ElementTree as ET
    tree = ET.fromstring(the_page)
    root = tree
    # for child in root:
    #     print child.tag
    #     if child.tag==u'{http://www.w3.org/2005/Atom}content':
    #         child = child[0]
    #         for child_child in child:
    #             print child_child
    #             if child_child.tag==u'{http://adriver.ru/ns/restapi/atom}stat':
    #                  for child_child_child in child_child:
    #                     print child_child_child
    clicks=get_stats(root,'{http://adriver.ru/ns/restapi/atom}click')
    views=get_stats(root,'{http://adriver.ru/ns/restapi/atom}exp')
    url='https://api.adriver.ru/stat/ads/'+str(avd_id)+'/total'
    print url
    headers = { 'X-Auth-userId': userId,
                'X-Auth-Passwd': token}
    #data = urllib.urlencode(values)
    req = urllib2.Request(url, headers=headers)
    response = urllib2.urlopen(req)
    the_page = response.read()
    import xml.etree.ElementTree as ET
    tree = ET.fromstring(the_page)
    root = tree
    reach=get_stats(root,'{http://adriver.ru/ns/restapi/atom}reach')
    return clicks, views, reach