from site_book_data import SiteBookData
import io
from lxml import etree
import requests

############ Scribd Site Class ################
"""parses the book data from Scribd"""
class ScribdSite:
    def __init__(self):
        pass
     
    def get_book_data_from_site(self,url):
        pass

    def find_matches_at_site(self,book_data):
        pass

    def convert_book_id_to_url(self,book_id):
        pass

    #------------ Utility Methods -------------
    def titleParser(self, content):
        parser = etree.HTMLParser(remove_pis=True)
        tree = etree.parse(io.BytesIO(content), parser)
        root = tree.getroot()
        print(root)
        title_element = root.xpath(".//h1[@class='document_title']")[0]
        title = title_element.text
        print(title)
        return title

    def subtitleParser(self,content):
        pass

    def authorsParser(self,content):
        parser = etree.HTMLParser(remove_pis=True)
        tree = etree.parse(io.BytesIO(content), parser)
        root = tree.getroot()
        author_elements = root.xpath(".//span[@class='author']")
        print(author_elements)
        authors = []
        for auth_element in author_elements:
            authors.append(auth_element.text)
            print(auth_element.text)
        return authors

    def isbnParser(self, content):
        parser = etree.HTMLParser(remove_pis=True)
        tree = etree.parse(io.BytesIO(content), parser)
        root = tree.getroot() 
        isbn_element = root.xpath("/html/head/meta[18]/@content")
        isbn = isbn_element[0]
        print(isbn)
        return isbn


    def formatParser(self, content):
        parser = etree.HTMLParser(remove_pis=True)
        tree = etree.parse(io.BytesIO(content), parser)
        root = tree.getroot() 
        format_element = root.xpath("/html/head/meta[13]/@content")
        form = format_element[0]
        print(form)
        return form
        

    def imageParserURL(content):
        pass

    def descParser(self, content):
        parser = etree.HTMLParser(remove_pis=True)
        tree = etree.parse(io.BytesIO(content), parser)
        root = tree.getroot() 
        desc_elements = root.xpath("/html/head/meta[16]/@content")
        desc = desc_elements[0]
        print(desc) 
        return desc

    def seriesParser(self, content):
        parser = etree.HTMLParser(remove_pis=True)
        tree = etree.parse(io.BytesIO(content), parser)
        root = tree.getroot()  
        series ='' 
        if root.xpath(""):
            series = root.xpath("")[0].text    
            series = series.strip().split('#')[0]
        print(series) #volume is include in the series, find a way return both.
        return series
        
    def volumeParser(content):
        pass

    def contentParser(content):
        pass # we already have this

    def saleReadyParser(content):
        pass

    def extraParser(content):
        pass

    def imageUrlParser(content):
        parser = etree.HTMLParser(remove_pis=True)
        tree = etree.parse(io.BytesIO(content), parser)
        root = tree.getroot() 
        imageUrlParser_element = root.xpath("/html/head/link[5]/@href")
        imageURL = imageUrlParser_element[0]
        print(imageURL) 
        return imageURL

    #parseAll parses all data, prints it, and 
    #stores it in a SiteBookData Object
    def parseAll(content, SiteBookData):
        pass

    def tester(content):
        print("Hello")
   
    ############# End of Class #################



def main():
    url = "https://www.scribd.com/book/205512285/A-Series-of-Unfortunate-Events-1-The-Bad-Beginning"
   # url = prompt("Enter a url");
    content = fetch(url)
    site = ScribdSite() 
    #site.titleParser(content)
    site.authorsParser(content)
    #site.isbnParser(content)
    #site.formatParser(content)
    #site.descParser(content)
    site.imageUrlParser(content)

  
def fetch(url):
    response = requests.get(url)
    return response.content








if __name__ == "__main__":
    main()










