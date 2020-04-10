import datetime as dt
import os

def clear():

    if os.name == "nt":
        command = "cls"
    
    else:
        command = "clear"

    os.system(command)


def get_now_time():

    #Get the current time in JST
    JST = dt.timezone(dt.timedelta(hours=+9), 'JST')
    now = dt.datetime.now(JST)

    month = now.month
    date = now.day
    hours = now.hour

    return [month, date, hours,]
