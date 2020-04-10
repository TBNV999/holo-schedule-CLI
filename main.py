#Fetch the schedule of hololive live stream

import os
import sys
import time

from src.fetch_html import *
from src.scraping import *
from src.util import *


def main():

    source_html = fetch_source_html()
    show_list(source_html)



if __name__ == '__main__':
    main()
