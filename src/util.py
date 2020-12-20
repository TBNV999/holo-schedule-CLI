import datetime as dt
import os
import sys


#Global
global OS_NAME 
OS_NAME = os.name


def add_zero(num):

    if num < 10:
        str_num = '0' + str(num)

    else:
        str_num = str(num)

    return str_num


def check_timezone():

    TIMEZONE_PATH = 'text/timezone'

    with open(TIMEZONE_PATH, 'r') as f:
        timezone = f.read().replace('\n', '')

    return timezone


def get_index_list(stream_members_list):

    JA_LIST = get_member_list()
    index_list = []
    length = len(stream_members_list)

    for i in range(length):
        index_list.append(JA_LIST.index(stream_members_list[i]))

    return index_list


def eval_argv(argv):

    valid_options_list = {'--help', '--eng', '--date', '--tomorrow', '--all'}

    #Options that is not available with other options
    special_options = {'--help', '--date'}

    #Options that is available to use other non special option at the same time
    non_special_options = {'--eng', '--tomorrow', '--all'}

    s_flag = 0
    n_flag = False

    for option in argv:

        if not option in valid_options_list:
            return None

        if option in special_options:
            s_flag += 1 

        if option in non_special_options:
            n_flag = True

        if s_flag and n_flag or s_flag > 1:

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

    return members_list


def get_now_time():

    #Get the current time in JST(UTC+9)
    JST = dt.timezone(dt.timedelta(hours=+9), 'JST')
    now = dt.datetime.now(JST)

    month = now.month
    date = now.day

    return (month, date)


def get_tomorrow():

    #Get the tomorrow date in JST
    JST = dt.timezone(dt.timedelta(hours=+9), 'JST')
    tomorrow = dt.datetime.now() + dt.timedelta(days=1)

    month = tomorrow.month
    date = tomorrow.day

    return (month, date)


def move_current_directory():

    #Move to the directory that has main.py
    #Change directory delimiter by OS

    #Windows
    if OS_NAME == 'nt':
        path = __file__.replace(r'\src\util.py', '')
        os.chdir(path)

    #POSIX
    else:
        path = __file__.replace('/src/util.py', '')
        os.chdir(path)


def option_check(options):

    eng_flag = False
    tomorrow_flag = False
    all_flag = False

    if '--help' in options:
        show_help()
        sys.exit()

    if '--date' in options:
        show_date()
        sys.exit()

    if '--eng' in options:
        eng_flag = True

    if '--tomorrow' in options:
        tomorrow_flag = True

    if '--all' in options:
        all_flag = True

    return (eng_flag, tomorrow_flag, all_flag)
        

def replace_name(members_list, length):

    for i in range(length):
        members_list[i] = members_list[i].replace('Sub','サブ')
        members_list[i] = members_list[i].replace('Risu','Ayunda Risu')
        members_list[i] = members_list[i].replace('Moona','Moona Hoshinova')
        members_list[i] = members_list[i].replace('Iofi','Airani Iofiteen')

    return members_list

def show_date():

    JST = dt.timezone(dt.timedelta(hours=+9), 'JST')
    now = dt.datetime.now(JST)

    month = now.month
    date = now.day
    hours = add_zero(now.hour)
    minutes = add_zero(now.minute)

    print('{}/{} {}:{} (JST)'.format(month, date, hours, minutes))


def show_help():

    with open('text/help', 'r') as f:
        
        l = f.read().split('\n')

        #Remove the message
        l.pop(0)

        for line in l:
            print(line)


#Show the schedule list in English
def show_in_english(time_list, stream_members_list, stream_url_list, timezone):

    en_members_list = get_en_list()
    index_list = get_index_list(stream_members_list)

    print('Index   Time       Member             Streaming URL   ({})'.format(timezone))

    #All three lists have the same length
    lists_length = len(time_list)

    for i in range(lists_length):

        if i < 10:
            space = ' '

        else:
            space = ''

        m_space = ' ' * ( (-1 * len(en_members_list[index_list[i]]) ) + 17)
        print('{}{}      {}~     {}{}  {}'.format(i, space, time_list[i], en_members_list[index_list[i]], m_space, stream_url_list[i]))


def timezone_convert(time_list, timezone):

    import pytz

    new_date_list = []
    hour_list = []
    minute_list = []

    length = len(time_list)

    for i in range(length):
        
        tmp = time_list[i].split(':')
        hour_list.append(int(tmp[0]))
        minute_list.append(int(tmp[1]))
        
    now = dt.datetime.now()
    year = now.year
    month = now.month
    day = now.day
    JST = pytz.timezone('Asia/Tokyo')

    new_date_list = list(map(lambda x: JST.localize(x), new_date_list))

    for i in range(length):

        new_date_list.append(dt.datetime(year, month, day, hour_list[i], minute_list[i]))

    new_timezone = pytz.timezone(timezone)

    new_date_list = list(map(lambda x: x.astimezone(new_timezone),new_date_list))

    new_hour_list = []
    new_minute_list = []
    new_time_list = []

    new_hour_list = list(map(lambda x: add_zero(x.hour), new_date_list))
    new_minute_list = list(map(lambda x: add_zero(x.minute), new_date_list))

    for i in range(length):

        new_time_list.append('{}:{}'.format(new_hour_list[i], new_minute_list[i]))

    return new_time_list
