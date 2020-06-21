#Generate today's stream list from html
import re
import time

from src.util import *

import requests


#Delete non-hololive stream
def delete_exception(time_list, stream_members_list, stream_url_list, is_all):

    EXCEPTION_LIST = {'Yogiri', 'Civia', 'SpadeEcho', 'Doris', 'Artia', 'Rosalyn'}
    length = len(time_list)

    if not is_all:
        #Slice to get only non-hololive members (e.g. holostars hololive-ID)
        EXCEPTION_LIST =  EXCEPTION_LIST | set(get_member_list()[29:])

    for i in range(length):

        if stream_members_list[i] in EXCEPTION_LIST:
            time_list[i] = None
            stream_members_list[i] = None
            stream_url_list[i] = None

    time_list = [i for i in time_list if not i is None]
    stream_members_list = [i for i in stream_members_list if not i is None]
    stream_url_list = [i for i in stream_url_list if not i is None]

    return time_list, stream_members_list, stream_url_list


def form_url(url):

    url = url.replace('"', '')
    url = url.replace('href=', '')

    return url


def scraping(source_html, is_all):

    pattern = re.compile('\d\d:\d\d')
    length = len(source_html)

    time_list = []
    stream_members_list = []
    stream_url_list = []

    for i in range(length):
        
        if not re.match(pattern, source_html[i]) is None:
            time_list.append(source_html[i])
            stream_members_list.append(source_html[i+1])
            stream_url_list.append(source_html[i-7])
            
    time_list, stream_members_list, stream_url_list = delete_exception(time_list, stream_members_list, stream_url_list, is_all)

    #Delete the noise data
    stream_url_list = list(map(form_url, stream_url_list))

    return time_list, stream_members_list, stream_url_list
