#Scrape today's schedule from Hololive official schedule

import sys

from src.util import *

import requests


def remove_text(text, date):

    text_list = text.split('\n')
    remove_list = [' ', '\r']

    #Delete null element and escape charactors and space in text_list
    for element in remove_list:
        text_list = tuple(map(lambda s: s.replace(element, ''),text_list))

    try:
        date_index = text_list.index(date)
    
    #Sometimes there is no streming on schedule
    except:
        sys.exit('No streaming found')


    text_list = text_list[date_index:]

    SPAN = '<divclass="holodulenavbar-text"style="letter-spacing:0.3em;">'

    try:
        last_index = text_list.index(SPAN)

    except ValueError:
        last_index = -10

    text_list = text_list[0:last_index]

    return text_list
 

#Fetch all stream in the day
def fetch_source_html(is_tomorrow):

    SOURCE_URL = 'http://bit.ly/hscli'
    #Temporary user agent
    HEADER = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'}

    if is_tomorrow:
        month, day = get_tomorrow()

    else:
        month, day = get_now_time()

    #Convert the time format to search source HTML 
    date = '{:02d}/{:02d}'.format(month, day)

    try:
        req = requests.get(SOURCE_URL, headers=HEADER, timeout=3)

    except Exception:
        sys.exit('Connection timeout')

    if req.status_code != 200:
        sys.exit('An error occured!')

    text_list = remove_text(req.text, date)

    return text_list
