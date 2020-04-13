import datetime as dt
import os

def clear():

    #Windows
    if os.name == 'nt':
        command = 'cls'
    
    #POSIX
    else:
        command = 'clear'

    os.system(command)


def eval_argv(argv):

    valid_options_list = ["--help", "--eng"]

    for option in argv:

        if not option in valid_options_list:
            return None

    return argv


def get_now_time():

    #Get the current time in JST
    JST = dt.timezone(dt.timedelta(hours=+9), 'JST')
    now = dt.datetime.now(JST)

    month = now.month
    date = now.day
    hours = now.hour

    return [month, date, hours]


def show_help():

