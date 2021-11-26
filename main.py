#Fetch the schedule of hololive live stream

import sys
import unicodedata

from src.fetch_html import *
from src.scraping import *
from src.util import *


def main(options):

    timezone = check_timezone()

    #Check options
    if options is None:

        eng_flag = False
        tomorrow_flag = False
        all_flag = False
        title_flag = False

    else:
        eng_flag, tomorrow_flag, all_flag, title_flag = option_check(options)

    #Fetch html file from https://schedule.hololive.tv/simple
    source_html = fetch_source_html(tomorrow_flag)
    time_list, members_list, url_list = scraping(source_html, all_flag)
    
    if timezone != 'Asia/Tokyo':
       time_list = timezone_convert(time_list, timezone)


    #All three lists have the same length
    lists_length = len(time_list)

    members_list = list(map(replace_name,members_list))
    hour_list = list(map(lambda x: int(x.split(':')[0]), time_list))

    #Check if date is shifted
    if hour_list != sorted(hour_list):
        date_shift = True
        shift_index = check_shift(hour_list)

    else:
        date_shift = False
        shift_index = (256, 256)
    
    title_list = []

    if title_flag:
        title_list = fetch_title(url_list)

    #Convert member's name into English
    if eng_flag:
        en_members_list = get_en_list()
        index_list = get_index_list(members_list)

        members_list = [en_members_list[member] for member in index_list]

    print('     Time      Member            Streaming URL          ({})'.format(timezone))


    for i, (time, member, url) in enumerate(zip(time_list,members_list,url_list)):


        if date_shift:

            if shift_index[0] == i - 1:

                if tomorrow_flag:
                    print('\nTomorrow\n')

                else:
                    print('\nToday\n')

            if shift_index[1] == i - 1:

                if tomorrow_flag:
                    print('\The day after tomorrow\n')

                else:
                    print('\nTomorrow\n')

        if i < 9:
            space = ' '

        else:
            space = ''

        #Check charactor type of member name
        #Contain Japanese
        if unicodedata.east_asian_width(members_list[i][0]) == 'W':
            m_space = ' ' * ( (-2 * len(members_list[i]) + 18))

        else:
            m_space = ' ' * ( (-1 * len(members_list[i]) ) + 18)

        #With titles of streams
        if title_flag:

            try:
                print('{}{}   {}~    {}{}{}  {}'.format(i+1, space, time, member, m_space, url, title_list[i]))

            #Some emoji cause this error
            except UnicodeEncodeError:
                title_list[i] = remove_emoji(title_list[i])
                print('{}{}   {}~    {}{}{}  {}'.format(i+1, space, time, member, m_space, url, title_list[i])) 

        else:
            print('{}{}   {}~    {}{}{}'.format(i+1, space, time_list[i], members_list[i], m_space, url_list[i]))



if __name__ == '__main__':

    argv = sys.argv

    move_current_directory()

    if len(argv) > 1:
        argv.pop(0)

        try:
            argv = set(eval_argv(argv))

        except TypeError:
            print('Invalid argument')
            sys.exit()

        # If inputed option is invalid eval_argv returns None
        if argv is None:
            print('Error: invalid options. Execute with --help to check about options')
            sys.exit()

        else:
            main(argv)

    #No option
    else:
        main(None)
