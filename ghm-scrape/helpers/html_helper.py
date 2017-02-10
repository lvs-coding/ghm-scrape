from bs4 import BeautifulSoup
import re
import string
from classes.Category import Category


from constants import Constants
    

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
                #parent_ul = hyperlink.findParent('ul')
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

def get_side_menu(soup):
    print 'get_side_menu'