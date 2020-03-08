from site_book_data import SiteBookData
import io
from lxml import etree
import requests
import re

############ TestSite Class ################
"""parses the book data from test bookstore"""
class TestSite:
    def __init__(self):
        self.site_slug = "TB"
        self.search_url = "http://127.0.0.1:8000/books/search/"
        self.url_to_book_detail ="http://127.0.0.1:8000/books/"
     
    def get_book_data_from_site(self,url):
        content = fetch(url)
        title = self.titleParser(content)
        author = self.authorsParser(content)
        subtitle = self.subtitleParser(content)
        isbn = self.isbnParser(content)
        frmt = self.formatParser(content)
        description = self.descParser(content)
        series = self.seriesParser(content)
        volume = self.volumeParser(content)
        sale_ready = self.saleReadyParser(content)
        price = self.priceParser(content)
        siteBookData = SiteBookData(content=content, book_title=title, authors=author, subtitle=subtitle, isbn_13=isbn, format=frmt,
         description=description, series=series, volume=volume, ready_for_sale=sale_ready, price=price)
        return siteBookData

        

    def find_matches_at_site(self,book_data):
        url =self.search_url
        print("url:", url)
        br = mechanize.Browser()
        br.set_handle_robots(False)
        br.open(url)  
        #selects the form to populate 
        br.select_form(class_="search-form")
        search_txt =''
        #populate the field. You may need to check if this is actually working
        if site_book_data.book_title:
            search_txt=site_book_data.book_title
        elif site_book_data.isbn13:
            search_txt= site_book_data.isbn_13
        elif site_book_data.authors:
            search_txt = site_book_data.authors[0]
        if not search_txt:
            return []
        br['query'] =search_txt
        
        #submit the form and get the returned page.
        res=br.submit()
        self.__get_book_data_from_page(res.read(), site_book_data)
        #return self.match_list # for testing I get the first page results only
        while(True):
            try:
                print("nextpage")
                res=br.follow_link(text="Next")
                self.__get_book_data_from_page(res.read(), site_book_data)
            except mechanize._mechanize.LinkNotFoundError:
                print("Reached end of results")
                return self.match_list
        return 

    def __get_book_data_from_page(self, content, book_site_dat_1):
        parser = etree.HTMLParser(remove_pis=True)
        tree = etree.parse(io.BytesIO(content), parser)
        root = tree.getroot()
        url_elements = root.xpath(".//p[@class='title product-field']/a/@href")

        for url in url_elements:
            #call function to get book data with url
            book_site_dat_tmp= self.get_book_data_from_site(url)
            score = self.match_percentage(book_site_dat_1, book_site_dat_tmp) 
            book_data_score =tuple([score,book_site_dat_tmp])
            #print('score', score)
            #book_site_dat_tmp.print_all()
            self.match_list.append(book_data_score)

    def convert_book_id_to_url(self,book_id):
        url = self.url+book_id
        return url

    #------------ Utility Methods -------------
    def titleParser(self, content):
        parser = etree.HTMLParser(remove_pis=True)
        tree = etree.parse(io.BytesIO(content), parser)
        root = tree.getroot()
        title_element = root.xpath(".//h1")[0]
        title = title_element.text
        return title

    def subtitleParser(self, content):
        parser = etree.HTMLParser(remove_pis=True)
        tree = etree.parse(io.BytesIO(content), parser)
        root = tree.getroot()
        subtitle_element = root.xpath("/html/body/div[3]/div/h2")[0]
        subtitle = subtitle_element.text
        return subtitle
        
        

    def authorsParser(self, content):
        parser = etree.HTMLParser(remove_pis=True)
        tree = etree.parse(io.BytesIO(content), parser)
        root = tree.getroot()
        author_element = root.xpath(".//h3")[0]
        author = author_element.text[3:]
        author = author.split(',')
        return author

    def isbnParser(self, content):
        parser = etree.HTMLParser(remove_pis=True)
        tree = etree.parse(io.BytesIO(content), parser)
        root = tree.getroot()
        isbn = root.xpath("/html/body/div[3]/div/div/h6[4]/text()")[0]
        return isbn

    def formatParser(self, content):
        parser = etree.HTMLParser(remove_pis=True)
        tree = etree.parse(io.BytesIO(content), parser)
        root = tree.getroot()
        format_type = root.xpath("/html/body/div[3]/div/div/h6[6]/text()")[0]
        return format_type

    def imageParser(self):
        pass

    def descParser(self, content):
        parser = etree.HTMLParser(remove_pis=True)
        tree = etree.parse(io.BytesIO(content), parser)
        root = tree.getroot()
        try: 
            desc_elements = root.xpath("/html/body/div[3]/div/div/p[@class='indent_this']/text()")[0]
        except IndexError:
            desc_elements = root.xpath("/html/body/div[3]/div/div/p/text()")
            full_desc = ""
            for desc in desc_elements:
                full_desc = full_desc+desc

            cleanr = re.compile('<.*?>')
            cleantext = re.sub(cleanr, ' ', full_desc)
            return cleantext
        

        return desc_elements

    def seriesParser(self, content):
        parser = etree.HTMLParser(remove_pis=True)
        tree = etree.parse(io.BytesIO(content), parser)
        root = tree.getroot()
        try: 
            series = root.xpath("/html/body/div[3]/div/div/h6[2]/text()")[0]
        except IndexError:
            series = "no series"
        
        return series

    def volumeParser(self, content):
        parser = etree.HTMLParser(remove_pis=True)
        tree = etree.parse(io.BytesIO(content), parser)
        root = tree.getroot()
        try: 
            volume = root.xpath("/html/body/div[3]/div/div/h6[3]/text()")[0]
        except IndexError:
            volume = "no volume"
        
        return volume

    def contentParser(self, url):
        content = fetch(url)
        return content
        

    def saleReadyParser(self, content):
        parser = etree.HTMLParser(remove_pis=True)
        tree = etree.parse(io.BytesIO(content), parser)
        root = tree.getroot()
        saleReady = root.xpath("/html/body/div[3]/div/div/p[@style='color: red;' or @style='color: green;']/text()")[0]
        return saleReady

    def priceParser(self, content):
        parser = etree.HTMLParser(remove_pis=True)
        tree = etree.parse(io.BytesIO(content), parser)
        root = tree.getroot()
        price = root.xpath("/html/body/div[3]/div/div/h6[1]/text()")[0]
        return price

    def extraParser(self):
        pass

    def imageUrlParser(self):
        pass

    #parseAll parses all data, prints it, and 
    #stores it in a SiteBookData Object
    def parseAll(self, url):
        url = "http://127.0.0.1:8000/books/30/"
        #url = prompt("Enter a url");
        content = fetch(url)
        site = TestSite() 
        print(site.titleParser(content))
        print(site.authorsParser(content))
        print(site.isbnParser(content))
        print(site.descParser(content))
        print(site.formatParser(content))
        print(site.subtitleParser(content))
        print(site.seriesParser(content))
        print(site.volumeParser(content))
        print(site.saleReadyParser(content))
        print(site.priceParser(content))

    def tester(self, content):
        print("Hello")
   

############# End of Class #################



def main():

    url = "http://127.0.0.1:8000/books/30/"
    BookSite = TestSite()
    content = fetch(url)
    #print(BookSite.formatParser(content))
    #BookSite.parseAll(content)
    BookSite.get_book_data_from_site(url).print_all()
    
    
    

  
def fetch(url):
    response = requests.get(url)
    return response.content

if __name__ == "__main__":
    main()