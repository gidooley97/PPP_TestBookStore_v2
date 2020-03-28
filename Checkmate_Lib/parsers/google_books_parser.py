from site_book_data import SiteBookData
import io
from lxml import etree
import requests
from PIL import Image
import requests
from io import BytesIO
import urllib.request
from bookSite import BookSite
import mechanize
import checkmate
from bookSite import BookSite
import re

class GoogleBooks(BookSite):
    def __init__(self):
        self.site_slug = "GB"
        self.search_url = "https://www.google.com/search?q=&source=lnms&tbm=bks&sa=X&ved=2ahUKEwj10bG89ZDoAhUEnKwKHcC4B-YQ_AUoAXoECBQQCQ&biw=1235&bih=634"
        self.url_to_book_detail = "https://www.books.google.com/book?vid=ISBN"
        self.match_list = []

    def get_book_data_from_site(self, url):
        content = requests.get(url).content
        parser = etree.HTMLParser(remove_pis=True)
        tree = etree.parse(io.BytesIO(content), parser)
        root = tree.getroot()
        frmt = self.format_parser(root)
        title = self.titleParser(root)
        img_url = self.imageUrlParser(root)
        img = self.imageParser(img_url)
        isbn13 = self.isbnParser(root)
        desc = self.descriptionParser(root)
        series = self.seriesParser(root)
        subtitle = self.subtitleParser(root)
        authors = self.authorsParser(root)
        site_slug = self.site_slug
        content = content
        url = url
        parse_status = self.get_parse_status(title, isbn13, desc, authors)
        ready_for_sale = self.sales_flag_parser(root)
        extra = self.extraParser(root)
        book_site_data = SiteBookData(format=frmt, book_title=title, book_img= img, book_img_url=img_url, isbn_13=isbn13, description=desc, series=series, 
        volume="", subtitle=subtitle, authors=authors, book_id=None, site_slug=site_slug, parse_status=parse_status, url=url, content=content,
        ready_for_sale=ready_for_sale, extra=extra)
        return book_site_data
    #for testing
    def get_book_data_from_site_v2(self, content):
        #content = requests.get(url).content
        parser = etree.HTMLParser(remove_pis=True)
        tree = etree.parse(io.BytesIO(content), parser)
        root = tree.getroot()
        frmt = self.format_parser(root)
        title = self.titleParser(root)
        img_url = self.imageUrlParser(root)
        img = self.imageParser(img_url)
        isbn13 = self.isbnParser(root)
        desc = self.descriptionParser(root)
        series = self.seriesParser(root)
        subtitle = self.subtitleParser(root)
        authors = self.authorsParser(root)
        site_slug = self.site_slug
        content = content
        #url = url
        parse_status = self.get_parse_status(title, isbn13, desc, authors)
        ready_for_sale = self.sales_flag_parser(root)
        extra = self.extraParser(root)
        book_site_data = SiteBookData(format=frmt, book_title=title, book_img= img, book_img_url=img_url, isbn_13=isbn13, description=desc, series=series, 
        volume="", subtitle=subtitle, authors=authors, book_id=None, site_slug=site_slug, parse_status=parse_status, url=None, content=content,
        ready_for_sale=ready_for_sale, extra=extra)
        return book_site_data

    def find_book_matches_at_site(self, site_book_data):
        url = self.search_url
        br = mechanize.Browser()
        br.set_handle_robots(False)
        br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
        res= br.open(url)

        #print(res.read())
        
        br.select_form(name="f")
        #print('form', br)
        search_txt = ''
        if site_book_data.book_title:
            search_txt=site_book_data.book_title
        elif site_book_data.isbn_13:
            search_txt = site_book_data.isbn_13
        elif site_book_data.authors:
            search_txt = site_book_data.authors[0]
        if not search_txt:
            return []
        br['q'] = search_txt

        res = br.submit()
        fileobj = open("page1.html","wb")#saves the returned page to a file. 
        #You can open and se the content
        content = res.read()
        fileobj.write(content)
        fileobj.close()
        self.__get_book_data_from_page(content,br, site_book_data)
        return self.match_list
        while(True):
            try:
                print("nextpage")
                res = br.follow_link(text="Next")
                self.__get_book_data_from_page(res.read(), br, site_book_data)
            except mechanize._mechanize.LinkNotFoundError:
                print("Reached end of results")
                return self.match_list

    def __get_book_data_from_page(self, content, br, book_site_dat_1):
        #print(content)
        parser = etree.HTMLParser(remove_pis=True)
        tree = etree.parse(io.BytesIO(content), parser)
        root = tree.getroot()
        url_elements = root.xpath('//a[@class="fuLhoc ZWRArf"]/@href')
        print("urls", len(url_elements))
        for url in url_elements:
            print('url',url)
            #book_site_dat_temp = self.get_book_data_from_site(url)

            book_site_dat_temp=self.navigate_to_view_ebook_page(br, url)
            if not book_site_dat_temp:
                continue
            score = self.match_percentage(book_site_dat_1, book_site_dat_temp)
            book_data_score = tuple([score,book_site_dat_temp])
            self.match_list.append(book_data_score)

    def navigate_to_view_ebook_page(self,br, url):
        content=br.open(url).read()
        parser = etree.HTMLParser(remove_pis=True)
        tree = etree.parse(io.BytesIO(content), parser)
        root = tree.getroot()
        if root.xpath('//p[@id="gb-get-book-not-available"]'):
            return 
        try:
            res=br.follow_link(text="View eBook")
        except mechanize._mechanize.LinkNotFoundError:
            try:
                return self.get_book_data_from_site(url)
            except:
                return
        fileobj = open("page1.html","wb")#saves the returned page to a file. 
        #You can open and se the content
        content = res.read()
        fileobj.write(content)
        fileobj.close()
        return self.get_book_data_from_site_v2(content)
        

    def convert_book_id_to_url(self, book_id):
        return self.url_to_book_detail+book_id

    def match_percentage(self, site_book1, site_book2):
        return super().match_percentage(site_book1, site_book2)

    def titleParser(self, root):
        title = root.xpath("//h1[@class='booktitle']//span//span")[0].text
        return title


    def subtitleParser(self, root):
        subtitle = ''
        if root.xpath("//h1[@class='booktitle']//span[2]//span"):
            subtitle = root.xpath("//h1[@class='booktitle']//span[2]//span")[0].text
        return subtitle

    def seriesParser(self, root):
        series = ''
        if root.xpath("//td[@class='metadata_value']/a[1]/i/span"):
            series = root.xpath("//td[@class='metadata_value']/a[1]/i/span")[0].text
        return series

    def authorsParser(self, root):
        author_elements = root.xpath("//div[@class='bookinfo_sectionwrap']/div[1]/a/span")
        authors = []
        for auth_element in author_elements:
            authors.append(auth_element.text)
        return authors

    def isbnParser(self, root):
        try:
            if root.xpath("//tr[4]//td[@class='metadata_label']//span")[0].text == 'ISBN':
                isbn_element = root.xpath("//tr[4]//td[@class='metadata_value']//span")[0].text
            elif root.xpath("//tr[5]//td[@class='metadata_label']//span")[0].text == 'ISBN':
                isbn_element = root.xpath("//tr[5]//td[@class='metadata_value']//span")[0].text
            elif root.xpath("//tr[6]//td[@class='metadata_label']//span")[0].text == 'ISBN':
                isbn_element = root.xpath("//tr[6]//td[@class='metadata_value']//span")[0].text
            elif root.xpath("//tr[7]//td[@class='metadata_label']//span")[0].text == 'ISBN':
                isbn_element = root.xpath("//tr[7]//td[@class='metadata_value']//span")[0].text
            isbns = str.split(isbn_element)
            return isbns[1]
        except:
            print("None found")
            return "None found"

    def descriptionParser(self, root):
        description = ''
        if root.xpath("//*[@id='synopsistext']"):
            description = root.xpath("//*[@id='synopsistext']")[0].text
        return description

    def imageUrlParser(self, root):
        try:
            imgUrl = root.xpath("//*[@id='summary-frontcover']/@src")[0]
            print(imgUrl)
        except:
            print("image url failed to parse")
            imgUrl = 'failed'
        return imgUrl

    def imageParser(self, url):
        image = None
        try:
            image = Image.open(urllib.request.urlopen(url))
        except:
            print("Image failed to load")
        return image

    def sales_flag_parser(self, root):
        sale_flag = 0
        status = ""
        sales_element = root.xpath("//*[@id='gb-get-book-content']")[0].text
        if "print" in sales_element.lower():
            sale_flag = 0
            status = "Find Print"
        elif "ebook" in sales_element.lower():
            status = 0
            status = "Buy Now"
        elif "pre-order" in sales_element.lower():
            sale_flag = 1
            status = "Pre-order"
        return status

    def format_parser(self, root):
        fmt = ""
        sales_element = root.xpath("//*[@id='gb-get-book-content']")[0].text
        if "print" in sales_element.lower():
            fmt = "Find Print"
        elif "ebook" in sales_element.lower():
            fmt = "Buy Now"
        elif "pre-order" in sales_element.lower():
            fmt = "Pre-order"
        return fmt

    def extraParser(self, root):
        return {}

    def volumeParser(self, root):
    #method to be overriden if necessary. 
        return None

        
    def get_parse_status(self, title, isbn13, desc, authors):
        if title and isbn13 and desc and authors:
            return "UNSUCCESSFUL"
        if title or isbn13 or desc or authors:
            return "PARTIALLY PARSED"
        return "FULLY PARSED"