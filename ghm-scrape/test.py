import sys
import urllib2
from bs4 import BeautifulSoup
from selenium import webdriver
import time

from private import Constants
from helpers.html_helper import get_categories2

def main():
    BASE_URL = Constants.BASE_URL
    categories = '';

    page = urllib2.urlopen(BASE_URL)
    dom = BeautifulSoup(page)

    categories_block = dom.find('div',id = 'categories_block_left')

    if(categories_block != None):
        driver = webdriver.Chrome()
        categories = get_categories2(categories_block)

        for cat in categories:
            print cat.name
            print cat.link
            print cat.level
            print '=========================='
        # for cat in categories:
        #     print cat.name

if __name__ == '__main__':
    sys.exit(main())

