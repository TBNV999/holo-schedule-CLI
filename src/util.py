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


def get_index_list(stream_members_list):

    JA_LIST = get_member_list()
    index_list = []
    length = len(stream_members_list)

    for i in range(length):
        index_list.append(JA_LIST.index(stream_members_list[i]))

    return index_list


def eval_argv(argv):

    valid_options_list = ["--help", "--eng"]

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

    #Get the current time in JST
    JST = dt.timezone(dt.timedelta(hours=+9), 'JST')
    now = dt.datetime.now(JST)

    month = now.month
    date = now.day
    hours = now.hour

    return (month, date, hours)


def show_help():

    with open('text/help', 'r') as f:
        
        for line in f.readlines():
            print(line)


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
