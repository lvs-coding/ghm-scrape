from bs4 import BeautifulSoup
import re
import string
from classes.Category import Category
from classes.Product import Product
from elementname import ElementName

import urllib2
from bs4 import BeautifulSoup


from constants import Constants

def product_info_exists(product_page_url,elementName):
    page = urllib2.urlopen(product_page_url)
    soup = BeautifulSoup(page)
    right_column = soup.find(id = 'pb-left-column')
    primary_block = soup.find(id = 'primary_block')
    exists = True


    for case in switch(elementName):
        if case(ElementName.TITLE):
            element = right_column.findChildren('h2')
            if element == None:
                exists = False
            return exists
            break
        if case(ElementName.SHORT_DESCRIPTION):
            element = right_column.find(id = 'short_description_content')
            if element == None:
                exists = False
            return exists
            break
        if case(ElementName.PRICE):
            element = right_column.find(id ='our_price_display')
            if element == None:
                exists = False
            return exists
        if case(ElementName.DISCOUNT):
            element = right_column.find(id='reduction_percent_display')
            if element == None:
                exists = False
            return exists
        if case(ElementName.DESCRIPTION):
            if primary_block.find(id='idTab1') == None:
                return False
            element = primary_block.find(id='idTab1')
            if element == None:
                exists = False
            return exists
        if case(ElementName.INSTRUCTIONS):
            # LVS - TODO
            return False
        if case(ElementName.NET_WEIGHT):
            # LVS - TODO
            return False
        if case():
            print 'Element name invalid'

def get_product(url):
    #product = Product(url)
    print '===== Scraping url : ' + url
    page = urllib2.urlopen(url)
    soup = BeautifulSoup(page)
    primary_block = soup.find(id = 'primary_block')
    right_column = soup.find(id = 'pb-left-column')
    left_column = soup.find(id = 'pd-right-column')
    
    non_decimal = re.compile(r'[^\d.]+')

    short_description = ''
    discount = ''
    description = ''

    title = right_column.findChildren('h2')[0].text
    if product_info_exists(url,ElementName.SHORT_DESCRIPTION):
        short_description = right_column.find(id = 'short_description_content').findChildren('p')[0].text
    price = non_decimal.sub('',right_column.find(id ='our_price_display').text)
    if product_info_exists(url, ElementName.DISCOUNT):
        discount = non_decimal.sub('',right_column.find(id='reduction_percent_display').text)
    if product_info_exists(url,ElementName.DESCRIPTION):
        description = primary_block.find(id='idTab1').text

    #descriptions = get_descriptions(primary_block.find(id='idTab1'))
    
    
    print "TITLE : " + title + "\n"
    print "SHORT DESCRIPTION : " + short_description + "\n"
    print "PRICE : " + price + "\n"
    print "DISCOUNT : " + discount + "\n"
    print "DESCRIPTION : " + description

    product = Product()
    product.name = title
    product.short_description = short_description
    product.price = price
    product.discount = discount
    product.description = description

    return product

def get_source_links(page_source):
    soup = BeautifulSoup(page_source)

    links_raw = soup.select('a.product_img_link')

    links = []

    for link in links_raw:
        link_href = link.get("href")
        print('Append link : ' + link_href)
        links.append(link_href)
    return links
    
def get_number_of_pages(pagination_block):
    if pagination_block == None:
        return 1
    page_next = pagination_block.find('li',id='pagination_next')
    last_page = page_next.find_previous_sibling('li').text
    return last_page

def get_categories(categories_block):
    categories = []    

    hyperlinks = categories_block.findAll('a')
    
    # Loop through all hyperlink in the categories block
    for hyperlink in hyperlinks:
    	level = 0
    	has_children = False

    	href = hyperlink.get('href').strip()
    	# Get the first parent ul
        grandfather = hyperlink.parent.parent
        title = hyperlink.get('title').strip().lower()
        # The source page is wrong, the title attribute can be empty sometimes, in this case
        # the title is in the tag text, we use 'next' to get it
        if title == '':
            title = hyperlink.next.strip().lower()
        # Just to avoid getting link that miss data becasue it could produce bugs later
        if title != '' and href != '':
        	# If the first parent ul has 'tree' as class it means it's a first level ul
            if grandfather.has_attr('class') and grandfather['class'][0].strip() == 'tree':
                level = 1
                # Check if the category has children
                if hyperlink.parent.findChild('ul') != None:
                    has_children = True
                else:
                	has_children = False
            else:
                level = 2
            category = Category(title, href,level,has_children)
            categories.append(category)
        # Log the links with some missing data
        else:
            f = open('wrong_categories.log', 'w')
            f.write('title : ' + title + ' | href : ' + href)  # python will convert \n to os.linesep
            f.close()
    return categories

class switch(object):
    def __init__(self, value):
        self.value = value
        self.fall = False

    def __iter__(self):
        """Return the match method once, then stop"""
        yield self.match
        raise StopIteration
    
    def match(self, *args):
        """Indicate whether or not to enter a case suite"""
        if self.fall or not args:
            return True
        elif self.value in args: # changed for v1.5, see below
            self.fall = True
            return True
        else:
            return False