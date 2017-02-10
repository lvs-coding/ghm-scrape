import sys
import urllib2
from bs4 import BeautifulSoup
from selenium import webdriver
import time

from private import Constants
from helpers.html_helper import get_categories

def main():
    BASE_URL = Constants.BASE_URL
    categories = '';

    page = urllib2.urlopen(BASE_URL)
    dom = BeautifulSoup(page)

    categories_block = dom.find('div',id = 'categories_block_left')

    if(categories_block != None):
        driver = webdriver.Chrome()
        # Get all categories
        categories = get_categories(categories_block)
        # Loop through categories
        for cat in categories:
            print '========= CATEGORY ========='
            print 'Name : ' + cat.name
            print 'Level : ' + str(cat.level)
            print 'Link : ' + cat.link
            print 'Has children : ' + str(cat.has_children)
            print '----------------------------'
            # We only follow categories that has no children to avoid duplicates
            if not cat.has_children:
                
                # Following the category link with Selenium
                driver.get(cat.link)
                # Wait for page load
                time.sleep(5)
                html = driver.page_source
                soup = BeautifulSoup(html)

                # Get product link
                links_raw = soup.select('a.product_img_link')
                links = []

                for link in links_raw:
                    link_href = link.get("href")
                    print '======LINK====== ' + link_href





    # get all categories
    #categories = get_categories(soup)

    # Loop through categories 
        # follow categorie link with selenium
            # Loop through pages and get all product links
                # for each product links get product details






if __name__ == '__main__':
    sys.exit(main())

