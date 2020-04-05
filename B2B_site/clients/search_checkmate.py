

import os
import sys

dir_of_interest = '/home/blaise/Desktop/Python_projects/PPP_D2D_Project/Checkmate_Lib'
modules = {}

sys.path.append(dir_of_interest)
for module in os.listdir(dir_of_interest):
    if '.py' in module and '.pyc' not in module:
        current = module.replace('.py', '')
        modules[current] = __import__(current)

get_book_site = modules['checkmate'].get_book_site
SiteBookData = modules['site_book_data'].SiteBookData


def search(**kwargs):
    print('Blaise')
    search_with_attr=True
    print(kwargs)
    if kwargs['url'] or  kwargs['book_title'] or kwargs['authors']  or kwargs['isbn_13']:
        return  
    if 'url' in kwargs:
        url = kwargs['url'] 
        if url:
            search_with_attr=False 
   #Change this to true to search by attribute
    slug = 'GB'
    if search_with_attr:
        bookSite = get_book_site(slug)
        matches= bookSite.find_book_matches_at_site(kwargs)
        
        for book in matches:
            print("=======================================================================================")
            book.print_all()

    else:
        book_site = get_book_site(slug) # seed Book Site object with slug
        print('url:',url)
        #url = "https://www.google.com/books/edition/Harry_Potter_and_the_Cursed_Child_Parts/tcSMCwAAQBAJ?hl=en"
        book_site_data = book_site.get_book_data_from_site(url) # Parse data from site
        book_site_data.print_all()
        matches = book_site.find_book_matches_at_site(book_site_data) # Get book matches
        for book in matches:
            print("=======================================================================================")
            print("Score: ", str(book[0]))
            book[1].print_all()


