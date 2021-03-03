#Generate today's stream list from html
import re
import time

from src.util import *

import requests


#Delete non-hololive stream
def delete_exception(time_list, members_list, stream_url_list):

    length = len(time_list)

    #Slice to get only non-hololive members (e.g. holostars hololive-ID)
    EXCEPTION_LIST = set(get_all_members_list()[33:])

    for i in range(length):

        if members_list[i] in EXCEPTION_LIST:
            time_list[i] = None
            members_list[i] = None
            stream_url_list[i] = None

    time_list = [i for i in time_list if not i is None]
    members_list = [i for i in members_list if not i is None]
    stream_url_list = [i for i in stream_url_list if not i is None]

    return time_list, members_list, stream_url_list


def form_url(url):

    url = url.replace('"', '')
    url = url.replace('href=', '')

    return url


def scraping(source_html, is_all):

    pattern = re.compile('\d\d:\d\d')
    length = len(source_html)

    time_list = []
    members_list = []
    stream_url_list = []

    for i in range(length):
        
        if not re.match(pattern, source_html[i]) is None:
            time_list.append(source_html[i])
            members_list.append(source_html[i+1])
            stream_url_list.append(source_html[i-7])
            
    if not is_all:
        time_list, members_list, stream_url_list = delete_exception(time_list, members_list, stream_url_list)

    #Delete the noise data
    stream_url_list = list(map(form_url, stream_url_list))

    return time_list, members_list, stream_url_list
