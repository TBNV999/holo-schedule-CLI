# Fetch the schedule of hololive live stream

import sys
import unicodedata
import argparse

from src.fetch_html import *
from src.scraping import *
from src.util import *

LABELS = ("Yesterday", "Today", "Tomorrow", "The day after tomorrow")

def main(args):

    if args.date:
        show_date()
        sys.exit(0)

    timezone = check_timezone()

    # Fetch html file from https://schedule.hololive.tv/simple
    source_html = fetch_source_html(args.tomorrow)
    time_list, members_list, url_list = scraping(source_html, args.all)

    if args.future and not args.tomorrow:
        hour_list = list(map(lambda x: int(x.split(':')[0]), time_list))
        filter_map = filter_future(hour_list)
    else:
        filter_map = [True] * len(time_list)
    
    if timezone != 'Asia/Tokyo':
        time_list = timezone_convert(time_list, timezone)
        date_delta = get_date_delta(timezone)
    else:
        date_delta = 0

    if args.tomorrow:
        date_delta += 1


    # All three lists have the same length
    lists_length = len(time_list)

    members_list = list(map(replace_name, members_list))
    hour_list = list(map(lambda x: int(x.split(':')[0]), time_list))

    # Check if date is shifted
    if hour_list != sorted(hour_list):
        shift_index = check_shift(hour_list)
    else:
        shift_index = None

    title_list = []

    if args.title:
        title_list = fetch_title(url_list)

    # Convert member's name into English
    if args.eng:
        members_list = convert_into_en_list(members_list)

    print('     Time      Member            Streaming URL          ({})'.format(timezone))


    for i, (time, member, url) in enumerate(zip(time_list, members_list, url_list)):
        if not filter_map[i]:
            continue

        if shift_index:
            if shift_index[0] == i - 1:
                print('\n' + LABELS[1+date_delta] + '\n')

            if shift_index[1] == i - 1:
                print('\n' + LABELS[2+date_delta] + '\n')

        # Check charactor type of member name
        # Contain Japanese
        if unicodedata.east_asian_width(members_list[i][0]) == 'W':
            m_space = ' ' * ( (-2 * len(members_list[i]) + 18))

        else:
            m_space = ' ' * ( (-1 * len(members_list[i]) ) + 18)

        # With titles of streams
        if args.title:

            try:
                print('{:2d}   {}~    {}{}{}  {}'.format(i+1, time, member, m_space, url, title_list[i]))

            # Some emoji cause this error
            except UnicodeEncodeError:
                title_list[i] = remove_emoji(title_list[i])
                print('{:2d}   {}~    {}{}{}  {}'.format(i+1, time, member, m_space, url, title_list[i])) 

        else:
            print('{:2d}   {}~    {}{}{}'.format(i+1, time_list[i], members_list[i], m_space, url_list[i]))



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
    parser.add_argument(
        "--future",
        action="store_true",
        default=False,
        help="Only show streams starting in the future",
    )
    args = parser.parse_args()

    main(args)
