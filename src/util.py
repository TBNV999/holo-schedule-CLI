import datetime as dt
import os
import sys
import unicodedata

#Global
global OS_NAME 
OS_NAME = os.name


def add_zero(num):

    if num < 10:
        str_num = '0' + str(num)

    else:
        str_num = str(num)

    return str_num


def get_index_list(stream_members_list):

    JA_LIST = get_member_list()
    index_list = []
    length = len(stream_members_list)

    for i in range(length):
        index_list.append(JA_LIST.index(stream_members_list[i]))

    return index_list


def eval_argv(argv):

    valid_options_list = {'--help', '--eng', '--date', '--tomorrow', '--all', '--est'}

    #Options that is not available with other options
    special_options = {'--help', '--date'}

    #Options that is available to use other non special option at the same time
    non_special_options = {'--eng', '--tomorrow', '--all', '--est'}

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
    est_flag = False

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

    if '--est' in options:
        est_flag = True

    return (eng_flag, tomorrow_flag, all_flag, est_flag)
        

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

#Show EST
def est_convert(time_list, stream_members_list, stream_url_list, eng_flag):
   hours_list = [i.split(':')[0] for i in time_list]
   minutes_list = [i.split(':')[1] for i in time_list]
   hours_list = list(map(int, hours_list))
   minutes_list.reverse()
   time_list_est = []

   for x in hours_list:  
       if x <= 13:
           x += 10
           x = str(x)
       else:
           x -= 14
           x = "0" + str(x)
       temp_list = []
       temp_list.append(x)
       temp_list.append(minutes_list.pop())
       temp_list = ":".join(temp_list)
       time_list_est.append(temp_list)
    
   lists_length = len(time_list)

   if eng_flag:
       show_in_english(time_list_est, stream_members_list, stream_url_list, True)
       sys.exit()

   else:
       stream_members_list = replace_name(stream_members_list, lists_length)

   print('Index   Time(EST)  Member              Streaming URL')
   for i in range(lists_length):

        if i < 9:
            space = ' '

        else:
            space = ''

        #Check charactor type of member name
        #Contain Japanese
        if unicodedata.east_asian_width(stream_members_list[i][0]) == 'W':
            m_space = ' ' * ( (-2 * len(stream_members_list[i]) + 18))

        else:
            m_space = ' ' * ( (-1 * len(stream_members_list[i]) ) + 18)

        print('{}{}      {}~     {}{}  {}'.format(i+1, space, time_list_est[i], stream_members_list[i], m_space, stream_url_list[i]))


   

#Show the schedule list in English
def show_in_english(time_list, stream_members_list, stream_url_list, est_flag):

    en_members_list = get_en_list()
    index_list = get_index_list(stream_members_list)
    
    if est_flag:
     print('Index   Time(EST)  Member             Streaming URL')
    else:
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
