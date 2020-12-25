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

    else:
        eng_flag, tomorrow_flag, all_flag = option_check(options)

    #Fetch html file from https://schedule.hololive.tv/simple
    source_html = fetch_source_html(tomorrow_flag)
    time_list, stream_members_list, stream_url_list = scraping(source_html, all_flag)
    
    if timezone != "Asia/Tokyo":
       time_list = timezone_convert(time_list, timezone)
       is_jst = False

    else:
        is_jst = True

    if eng_flag:
        show_in_english(time_list, stream_members_list, stream_url_list, timezone)
        sys.exit()

        
    #All three lists have the same length
    lists_length = len(time_list)

    stream_members_list = replace_name(stream_members_list, lists_length)
    hour_list = list(map(lambda x: int(x.split(':')[0]), time_list))

    if hour_list != sorted(hour_list):
        date_shift = True
        shift_index = check_shift(hour_list)

    else:
        date_shift = False
        shift_index = (256, 256)

    # Show in Japanese
    print('Index   Time       Member              Streaming URL  ({})'.format(timezone))


    for i in range(lists_length):

        if date_shift:

            if shift_index[0] == i - 1:
                print('\nToday\n')

            if shift_index[1] == i - 1:
                print('\nTomorrow\n')

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

        print('{}{}      {}~     {}{}  {}'.format(i+1, space, time_list[i], stream_members_list[i], m_space, stream_url_list[i]))


if __name__ == '__main__':

    argv = sys.argv

    move_current_directory()

    if len(argv) > 1:
        argv.pop(0)

        try:
            argv = set(eval_argv(argv))

        except TypeError:
            print("Invalid argument")
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
