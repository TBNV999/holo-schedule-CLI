#Fetch the schedule of hololive live stream

import os
import sys

from src.fetch_html import *
from src.scraping import *
from src.util import *


def main(options):

    if not options is None:

        if "--help" in options:
            show_help()
            sys.exit()

        if "--eng" in options:
            eng = True

    else:
        eng = False

    source_html = fetch_source_html()
    time_list, stream_members_list, stream_url_list = get_list(source_html)

    if eng:
        show_in_english(time_list, stream_members_list, stream_url_list)
        sys.exit()

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

    if len(argv) > 1:
        argv.pop(0)
        argv = eval_argv(argv)

        if argv is None:
            print("Error: invalid options")
            sys.exit()

        else:
            main(argv)

    else:
        main(None)
