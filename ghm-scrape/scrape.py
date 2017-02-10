import sys
import urllib2
from bs4 import BeautifulSoup
from selenium import webdriver
import time

from private import PrivateData
from constants import Constants
from helpers.html_helper import get_categories
from helpers.html_helper import get_number_of_pages
from helpers.html_helper import get_source_links
from helpers.html_helper import get_product

def main():
    BASE_URL = PrivateData.BASE_URL
    categories = '';
    products_links = []

    page = urllib2.urlopen(BASE_URL)
    dom = BeautifulSoup(page)

    categories_block = dom.find('div',id = 'categories_block_left')

    if(categories_block != None):
        driver = webdriver.Chrome()
        # Get all categories
        categories = get_categories(categories_block)
        # Loop through categories
        for cat in categories:
            if cat.name != Constants.CATEGORY_TO_EXCLUDE:
                print '========= SCRAPING CATEGORY ========='
                print 'Name : ' + cat.name
                print 'Level : ' + str(cat.level)
                print 'Link : ' + cat.link
                print 'Has children : ' + str(cat.has_children)                
                # We only follow categories that has no children to avoid duplicates
                if not cat.has_children:
                    
                    # Following the category link with Selenium
                    driver.get(cat.link)
                    # Wait for page load
                    time.sleep(5)
                    html = driver.page_source
                    dom = BeautifulSoup(html)

                    page_next = dom.find('li',id='pagination_next')
                    last_page = 1
                    if(page_next != None):
                        last_page = int(page_next.find_previous_sibling('li').text)

                    number_of_pages = last_page 

                    print 'Number of pages : ' + str(number_of_pages)
                    print '--'
                    
                    for current_page in range (1,number_of_pages + 1):
                        print '--------- PAGE ' + str(current_page) + '---------'
                        # No page number for page 1
                        if(current_page == 1):
                            page_url = cat.link
                        else:
                            # Add pagination string to base url
                            page_url = cat.link + '#/page-' + str(current_page)
                        print 'page URL : ' + page_url
                        # Open page with Selenium
                        driver.get(page_url)
                        # Wait for page fully loaded
                        time.sleep(5)

                        # Get page source
                        html = driver.page_source

                        # Get all useful links from current page
                        page_links = get_source_links(html)
                        products_links.extend(page_links)

        # We don't need Selenium anymore
        driver.close()

        file_products = open('products.txt', 'w')
        for link in products_links:
            print '====== Product URL : ' + link
            formatted_link = link + '\n'
            product = get_product(link)

            print 'name : ' + product.name
            file_products.write(product.name.encode('utf8') + '\n')
            print 'short description : ' + product.short_description
            file_products.write(product.short_description.encode('utf8') + '\n')
            print 'price : ' + product.price
            file_products.write(product.price.encode('utf8') + '\n')
            print 'discount : ' + product.discount
            file_products.write(product.discount.encode('utf8') + '\n')
            print 'description : ' + product.description
            file_products.write(product.description.encode('utf8') + '\n')

        file_products.close()
if __name__ == '__main__':
    sys.exit(main())

