#Scrape today's schedule from Hololive official schedule

import os
import sys

from src.util import *

import requests


def convert_time(month, date):

    if month < 10:
        month = '0' + str(month)

    else:
        month = str(month)

    if date < 10:
        date = '0' + str(date)

    else:
        date = str(date)

    return '{}/{}'.format(month, date)


def remove_text(text, today):

    text_list = text.split('\n')

    #Delete null element and escape charactors and space in text_list
    text_list = tuple(map(lambda s: s.replace(' ', ''), text_list))
    text_list = tuple(map(lambda s: s.replace('\r', ''), text_list))
    text_list = tuple(map(lambda s: s.replace(' ', ''), text_list))

    today_index = text_list.index(today)
    text_list = text_list[today_index:]

    SPAN = '<divclass="holodulenavbar-text"style="letter-spacing:0.3em;">'

    try:
        last_index = text_list.index(SPAN)

    except ValueError:
        last_index = -10

    text_list = text_list[0:last_index]

    return text_list
 

#Fetch today's all stream
def fetch_source_html():

    SOURCE_URL = 'https://schedule.hololive.tv/simple'
    #Temporary user agent
    HEADER = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'}
    month, date = get_now_time()

    #Convert the time format to search source HTML 
    today = convert_time(month, date)

    try:
        req = requests.get(SOURCE_URL, headers=HEADER, timeout=3)

    except Exception:
        print("Connection timeout")
        sys.exit()

    if req.status_code != 200:
        print("An error occured!")
        sys.exit()

    text_list = remove_text(req.text, today)

    return text_list
