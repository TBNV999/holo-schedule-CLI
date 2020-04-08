#Scrape today's schedule from Hololive official schedule

import datetime as dt
import os
import sys

#External library
import requests
from bs4 import BeautifulSoup


def get_now_time():

    #Get the current time in JST
    JST = dt.timezone(dt.timedelta(hours=+9), 'JST')
    now = dt.datetime.now(JST)

    month = now.month
    date = now.day
    hours = now.hour
    minutes = now.minutes

    return [month, date, hours, minutes]


def convert_time(month, date, day):

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

    #Delete null element in text_list
    text_list = filter(lambda t: t != '', text_list)

    #Remove all space in text_list
    text_list = list(map(lambda s: s.replace(' ', ''), text_list))


#Fetch today's all stream
def fetch_today_list():

    SOURCE_URL = 'https://schedule.hololive.tv/simple'
    month, date, hours, minutes = get_now_time()

    #Convert the time format to search source HTML 
    today = convert_time(month, date)

    try:
        req = requests.get(SOURCE_URL, timeout=3)

    except Exception:
        print("Connection timeout")
        sys.exit()

    if req.status_code != 200:
        print("An error occured!")
        sys.exit()
