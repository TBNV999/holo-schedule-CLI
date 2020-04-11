#Show today's stream list from html
import re
import time

import requests


def get_member_list():

    MEMBER_FILE_PATH = 'text/hololive_members.txt'

    with open(MEMBER_FILE_PATH, 'r') as f:

        #Ignore the message of the first row
        members_list = f.readlines()[1].split(',')
        #Delete break symbol
        members_list[-1] = members_list[-1].replace('\n', '')

    return members_list


#Delete non-hololive stream
def delete_exception(time_list, stream_members_list, stream_url_list):

    SOURCE_MEMBER_LIST = get_member_list()

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


def scraping(source_html):

    pattern = re.compile('\d\d:\d\d')

    time_list = []
    stream_members_list = []
    stream_url_list = []

    for i in range(len(source_html)):
        
        if not re.match(pattern, source_html[i]) is None:
            time_list.append(source_html[i])
            stream_members_list.append(source_html[i+1])
            stream_url_list.append(source_html[i-7])
            
    time_list, stream_members_list, stream_url_list = delete_exception(time_list, stream_members_list, stream_url_list)

    #Delete first noise data
    stream_url_list = list(map(form_url, stream_url_list))

    return time_list, stream_members_list, stream_url_list


def get_list(source_html):

    time_list, stream_members_list, stream_url_list = scraping(source_html)

    return time_list, stream_members_list, stream_url_list
    #hour_list = list(map(lambda x: int(x.split(':')[0]), time_list))
