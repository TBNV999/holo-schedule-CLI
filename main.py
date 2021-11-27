#Fetch the schedule of hololive live stream

import sys
import unicodedata
import argparse

from src.fetch_html import *
from src.scraping import *
from src.util import *


def main(args):

    if args.date:
        show_date()
        sys.exit(0)

    timezone = check_timezone()

    #Fetch html file from https://schedule.hololive.tv/simple
    source_html = fetch_source_html(args.tomorrow)
    time_list, members_list, url_list = scraping(source_html, args.all)
    
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

    if args.title:
        title_list = fetch_title(url_list)

    #Convert member's name into English
    if args.eng:
        en_members_list = get_en_list()
        index_list = get_index_list(members_list)

        members_list = [en_members_list[member] for member in index_list]

    print('     Time      Member            Streaming URL          ({})'.format(timezone))


    for i, (time, member, url) in enumerate(zip(time_list,members_list,url_list)):


        if date_shift:

            if shift_index[0] == i - 1:

                if args.tomorrow:
                    print('\nTomorrow\n')

                else:
                    print('\nToday\n')

            if shift_index[1] == i - 1:

                if args.tomorrow:
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
        if args.title:

            try:
                print('{}{}   {}~    {}{}{}  {}'.format(i+1, space, time, member, m_space, url, title_list[i]))

            #Some emoji cause this error
            except UnicodeEncodeError:
                title_list[i] = remove_emoji(title_list[i])
                print('{}{}   {}~    {}{}{}  {}'.format(i+1, space, time, member, m_space, url, title_list[i])) 

        else:
            print('{}{}   {}~    {}{}{}'.format(i+1, space, time_list[i], members_list[i], m_space, url_list[i]))



if __name__ == '__main__':

    move_current_directory()

    parser = argparse.ArgumentParser(
        description="Hololive schedule scraping tool",
        formatter_class=argparse.RawTextHelpFormatter,
        epilog="""Notes: You cannot use --date with other options.
       But it is available to use the other options at the same time.

LICENSE: GNU General Public License v3.0

Github: https://github.com/TeepaBlue/holo-schedule-CLI""",
    )
    parser.add_argument(
        "--eng",
        action="store_true",
        default=False,
        help="Make displayed hololive member's name English",
    )
    parser.add_argument(
        "--date", action="store_true", default=False, help="Get the current time in JST"
    )
    parser.add_argument(
        "--tomorrow",
        action="store_true",
        default=False,
        help="Show tomorrow's schedule list",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        default=False,
        help="Show all available live streaming schedule including holostars, etc.",
    )
    parser.add_argument(
        "--title",
        action="store_true",
        default=False,
        help="Show schedule with the titles of the streams",
    )
    args = parser.parse_args()

    main(args)
