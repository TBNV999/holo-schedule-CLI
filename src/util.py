import datetime as dt
import os
import sys


#Global
OS_NAME = os.name


def clear():

    #Windows
    if OS_NAME == 'nt':
        command = 'cls'
    
    #POSIX
    else:
        command = 'clear'

    os.system(command)


def get_index_list(stream_members_list):

    JA_LIST = get_member_list()
    index_list = []
    length = len(stream_members_list)

    for i in range(length):
        index_list.append(JA_LIST.index(stream_members_list[i]))

    return index_list


def eval_argv(argv):

    valid_options_list = ['--help', '--eng', '--date']

    for option in argv:

        if not option in valid_options_list:
            return None

    return argv


def get_en_list():

    EN_FILE_PATH = 'text/hololive_members_en.txt'

    with open(EN_FILE_PATH, 'r') as f:

        #Ignore the message of the first row
        en_list = f.readlines()[1].split(',')

    #Delete break symbol
    en_list[-1] = en_list[-1].replace('\n', '')

    return tuple(en_list)


def get_member_list():

    MEMBER_FILE_PATH = 'text/hololive_members.txt'

    with open(MEMBER_FILE_PATH, 'r') as f:

        #Ignore the message of the first row
        members_list = f.readlines()[1].split(',')

    #Delete break symbol
    members_list[-1] = members_list[-1].replace('\n', '')

    return tuple(members_list)


def get_now_time():

    #Get the current time in JST(UTC+9)
    JST = dt.timezone(dt.timedelta(hours=+9), 'JST')
    now = dt.datetime.now(JST)

    month = now.month
    date = now.day
    hours = now.hour

    return (month, date, hours)


def move_current_directory():

    #Move to the directory that contains main.py
    #Change directory delimiter by OS

    #Windows
    if OS_NAME == 'nt':
        path = __file__.replace(r'\src\util.py', '')
        os.chdir(path)

    #POSIX
    else:
        path = __file__.replace('/src/util.py', '')
        os.chdir(path)
        

def show_date():

    JST = dt.timezone(dt.timedelta(hours=+9), 'JST')
    now = dt.datetime.now(JST)

    month = now.month
    date = now.day
    hours = now.hour
    minutes = now.minute

    if hours < 10:
        hours = '0' + str(hours)

    if minutes < 10:
        minutes = '0' + str(minutes)

    print('{}/{} {}:{} (JST)'.format(month, date, hours, minutes))


def show_help():

    with open('text/help', 'r') as f:
        
        l = f.read().split('\n')

        #Remove the message
        l.pop(0)

        for line in l:
            print(line)


#Show the schedule list in English
def show_in_english(time_list, stream_members_list, stream_url_list):

    en_members_list = get_en_list()
    index_list = get_index_list(stream_members_list)

    print('Index   Time(JST)  Member             Streaming URL')

    #All three lists have the same length
    lists_length = len(time_list)

    for i in range(lists_length):

        if i < 10:
            space = ' '

        else:
            space = ''

        m_space = ' ' * ( (-1 * len(en_members_list[index_list[i]]) ) + 17)
        print('{}{}      {}~     {}{}  {}'.format(i, space, time_list[i], en_members_list[index_list[i]], m_space, stream_url_list[i]))
