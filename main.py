#Fetch the schedule of hololive live stream

import sys

from src.fetch_html import *
from src.scraping import *
from src.util import *


def main(options):


    #Option flags
    eng_flag = False
    tomorrow_flag = False
    all_flag = False
    if not options is None:

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

    #Fetch html file from https://schedule.hololive.tv/simple
    source_html = fetch_source_html(tomorrow_flag)
    time_list, stream_members_list, stream_url_list = get_list(source_html, all_flag)

    if eng_flag:
        show_in_english(time_list, stream_members_list, stream_url_list)
        sys.exit()

    # Show in Japanese
    print('Index   Time(JST)  Member          Streaming URL')

    #All three lists have the same length
    lists_length = len(time_list)

    for i in range(lists_length):

        if i < 10:
            space = ' '

        else:
            space = ''

        m_space = ' ' * ( (-2 * len(stream_members_list[i]) + 14))
        print('{}{}      {}~     {}{}  {}'.format(i, space, time_list[i], stream_members_list[i], m_space, stream_url_list[i]))


if __name__ == '__main__':

    argv = sys.argv

    move_current_directory()

    if len(argv) > 1:
        argv.pop(0)
        argv = eval_argv(argv)

        # If inputed option is invalid eval_argv returns None
        if argv is None:
            print('Error: invalid options')
            sys.exit()

        else:
            main(argv)

    #No option
    else:
        main(None)
