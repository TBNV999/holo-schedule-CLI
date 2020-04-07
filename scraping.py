#Scrape today's schedule from Hololive official schedule

import datetime as dt
import os
import sys

import requests
from bs4 import BeautifulSoup


def get_now_time():

    #Get the time in JST
    JST = dt.timezone(dt.timedelta(hours=+9), 'JST')
    now = dt.datetime.now(JST)

    month = now.month
    date = now.day
    hours = now.hour
    minutes = now.minutes
    day = now.weekday()

    return [month, day, hours, minutes]


def convert_time(month, date, day):

    if month < 10:
        month = '0' + str(month)

    else:
        month = str(month)

    if date < 10:
        date = '0' + str(date)

    else:
        date = str(date)

    #Japanese day of week
    DAY_LIST = ['月', '火', '水', '木', '金', '土', '日']

    return '{}/{} ({})'.format(month, date, DAY_LIST[day])


#Fetch today's all stream
def fetch_today_list():

    SOURCE_URL = 'https://schedule.hololive.tv/simple'
    month, date, hours, minutes, day = get_now_time()

    #Convert the time to Japanese format time scraping
    today = convert_time(month, date, day) 

    

    try:
        req = requests.get(SOURCE_URL, timeout=3)

    except Exception:
        print("Connection timeout")
        sys.exit()

    if req.status_code != 200:
        print("An error occured!")
        sys.exit()
