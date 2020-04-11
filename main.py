#Fetch the schedule of hololive live stream

import os
import sys
import time

from src.fetch_html import *
from src.scraping import *
from src.util import *


def main():

    source_html = fetch_source_html()
    time_list, stream_members_list, stream_url_list = get_list(source_html)

    print('Index   Time(JST)  Member          Stream_URL')

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
    main()
