#Generate today's stream list from html
import re
import time

from src.util import *

import requests


#Delete non-hololive stream
def delete_exception(time_list, stream_members_list, stream_url_list):

    SOURCE_MEMBER_LIST = get_member_list()[0:28]

    for i in range(len(time_list)):

        if not stream_members_list[i] in SOURCE_MEMBER_LIST:
            time_list[i] = 'DELETE'
            stream_members_list[i] = 'DELETE'
            stream_url_list[i] = 'DELETE'

    time_list = [i for i in time_list if i != 'DELETE']
    stream_members_list = [i for i in stream_members_list if i != 'DELETE']
    stream_url_list = [i for i in stream_url_list if i != 'DELETE']

    return time_list, stream_members_list, stream_url_list


def form_url(url):

    url = url.replace('"', '')
    url = url.replace('href=', '')

    return url


def scraping(source_html, is_all):

    pattern = re.compile('\d\d:\d\d')

    time_list = []
    stream_members_list = []
    stream_url_list = []

    for i in range(len(source_html)):
        
        if not re.match(pattern, source_html[i]) is None:
            time_list.append(source_html[i])
            stream_members_list.append(source_html[i+1])
            stream_url_list.append(source_html[i-7])
            
    if not is_all:
        time_list, stream_members_list, stream_url_list = delete_exception(time_list, stream_members_list, stream_url_list)

    #Delete the first noise data
    stream_url_list = list(map(form_url, stream_url_list))

    return time_list, stream_members_list, stream_url_list


def get_list(source_html, is_all):

    time_list, stream_members_list, stream_url_list = scraping(source_html, is_all)

    return time_list, stream_members_list, stream_url_list
