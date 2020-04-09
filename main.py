#Fetch the schedule of hololive live stream

import os
import sys

from src.scraping import *
from src.fetch_html import *


def clear():

    if os.name == "nt":
        command = "cls"
    
    else:
        command = "clear"

    os.system(command)


def main():

    source_html = fetch_source_html()
    show_list(source_html)


if __name__ == '__main__':
    main()
