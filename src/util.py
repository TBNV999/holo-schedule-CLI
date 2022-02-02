import datetime as dt
import os
import sys
import unicodedata
import pathlib

from contextlib import redirect_stdout

import requests


# Global
global OS_NAME 
OS_NAME = os.name
    
JST = dt.timezone(dt.timedelta(hours=+9), 'JST')


def check_shift(hour_list):

    length = len(hour_list)
    today = 256
    tomorrow = 256

    for i in range(length - 1):
        
        tmp = i + 1

        if hour_list[i] > hour_list[tmp]:

            if len(hour_list[:i]) < len(hour_list[i:]):
                today = i
                break

            else:
                tomorrow = i
                break

    return (today, tomorrow)


def filter_future(hour_list):
    ret = []
    now = dt.datetime.now(JST)
    for hour in hour_list:
        ret.append(hour >= now.hour)
    return ret


def check_timezone():

    TIMEZONE_PATH = 'text/timezone'

    with open(TIMEZONE_PATH, 'r') as f:
        timezone = f.read().replace('\n', '')

    return timezone


def get_index_list(members_list):

    JA_LIST = get_all_members_list()

    index_list = tuple([JA_LIST.index(member.replace("サブ", "")) for member in members_list])

    return index_list


def fetch_title(url_list):

    title_list = []

    for url in url_list:

        # Check if the stream url is YouTube url
        if not "youtube" in url:
            title_list.append("")
            continue

        else:

            tmp = requests.get('https://www.youtube.com/oembed?url={}&format=json'.format(url))
            try:
                title = str(eval(tmp.text)['title'])
            except:
                title_list.append("")
                continue

            if unicodedata.east_asian_width(title[0]) != 'W':
                title = ' ' + title

            title_list.append(title)

    return title_list


def get_en_list():

    EN_FILE_PATH = 'text/hololive_members_en.txt'

    with open(EN_FILE_PATH, 'r') as f:

        # Ignore the message of the first row
        en_list = f.readlines()[1].split(',')

    # Delete break symbol
    en_list[-1] = en_list[-1].replace('\n', '')

    return tuple(en_list)


def get_all_members_list():

    MEMBER_FILE_PATH = 'text/hololive_members.txt'
    all_members_list = []

    with open(MEMBER_FILE_PATH, 'r') as f:
        # Ignore the message of the first row
        file_content = f.readlines()[1:]

    for member_block in file_content:
        all_members_list.extend(member_block.split(','))

    # Delete break symbol
    all_members_list[-1] = all_members_list[-1].replace('\n', '')

    return all_members_list


def get_now_time():

    # Get the current time in JST(UTC+9)
    now = dt.datetime.now(JST)

    month = now.month
    date = now.day

    return (month, date)

def get_date_delta(timezone):
    now = dt.datetime.now(JST).date()
    import pytz
    try:
        tz = pytz.timezone(timezone)
    except:
        sys.exit('Invalid timezone')
    now_ = dt.datetime.now(tz).date()
    return (now - now_).days

def get_hololive_members():

    MEMBER_FILE_PATH = 'text/hololive_members.txt'
    
    with open(MEMBER_FILE_PATH, 'r') as f:
        hololive_members_list = f.readlines()[1].split(',')

    #Delete the break symbol in the last member
    hololive_members_list[-1] = hololive_members_list[-1].replace('\n', '')

    return hololive_members_list


def get_tomorrow():

    # Get the tomorrow date in JST
    tomorrow = dt.datetime.now(JST) + dt.timedelta(days=1)

    month = tomorrow.month
    date = tomorrow.day

    return (month, date)


def move_current_directory():

    # Move to the directory that has main.py
    # Change directory delimiter by OS

    path = pathlib.Path(os.path.dirname(__file__)).parent
    os.chdir(path)


def remove_emoji(title):
    
    # Redirect to null in order not display
    with redirect_stdout(open(os.devnull, 'w')):
        tmp = []
        for i in list(title):
            try:
                print(i)
                tmp.append(i)
            except UnicodeEncodeError:
                pass
    title = ''.join(tmp)
    if len(title) == 0:
        title.append(' ')
    return title


def replace_name(member):

    member = member.replace('Sub','サブ')

    return member


def show_date():

    now = dt.datetime.now(JST)

    print(now.strftime("%m/%d %H:%M (JST)"))


def timezone_convert(time_list, timezone):
    import pytz

    new_date_list = []

    now = dt.datetime.now(JST)
    year = now.year
    month = now.month
    day = now.day

    new_date_list = [dt.datetime.strptime(t, '%H:%M').replace(year=year, month=month, day=day) for t in time_list]
    new_date_list = list(map(lambda x: pytz.timezone("Asia/Tokyo").localize(x), new_date_list))

    try:
        new_timezone = pytz.timezone(timezone)
    except:
        sys.exit('Invalid timezone')

    new_date_list = tuple(map(lambda x: x.astimezone(new_timezone), new_date_list))
    new_time_list = tuple([d.strftime("%H:%M") for d in new_date_list])

    return new_time_list
