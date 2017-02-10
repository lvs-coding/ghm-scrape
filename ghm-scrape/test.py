import sys
import urllib2
from bs4 import BeautifulSoup
from selenium import webdriver
import time
from classes.Product import Product

def main():
   
    product = Product()
    product.name = 'fdsfds'
    print product.name

    

    #number_of_pages = get_number_of_pages(pagination_block)
    #print 'Number of pages : ' + str(number_of_pages)

if __name__ == '__main__':
    sys.exit(main())

