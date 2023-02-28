import storage
import jsons_wtiter

import requests
from bs4 import BeautifulSoup
from fake_headers import Headers

import io
import arrow

domain_name = 'https://www.global.jdsports.com'

headers = Headers(
        browser="chrome", 
        os="win", 
        headers=False).generate()

def get_date():
    return arrow.now().format('YYMMDD,HH-mm-ss')

def url(count_from:int):
    return f'https://www.global.jdsports.com/men/brand/adidas-originals,nike,the-north-face,polo-ralph-lauren,jordan,champion,new-balance,napapijri/sale/?from={str(count_from)}&jd_sort_order=price-low-high&max=204'

def get_html(url):
    return requests.get(url, headers=headers).text

def get_soup(count_from:int):
    return BeautifulSoup(get_html(url(count_from)), 'lxml')

def find_not_found(page:BeautifulSoup):
    result = page.find('div', class_='not-found')
    if result == None:
        print('Page has a product')
        return True
    else:
        print('Page "404", process completed!')
        print(get_date())
        return False

def response(url:str):
    try:
        requests.get(url, headers=headers)
        print('Response received')
        return True
    except:
        print('No Response')
        return False

class Scraper:
    def __init__(self):
        self.set_soup(0) # правильно ли, вызывать метод в кострукторе, который иницализирует поле?
        self.table_items = self.soup.find('ul', class_='listProducts').find_all('li', class_='productListItem')
        self.dict_product_items = dict()

    def set_soup(self, count_from):
        self.soup = get_soup(count_from)

    def _get_data(self, table: set[BeautifulSoup]):
        for item in table:
            name_product = item.find('span', class_='itemTitle').text.replace('\n','')
            sku = item.find('span', class_='itemContainer').get('data-productsku')
            url_product = item.find('span', class_='itemTitle').find('a').get('href')

            price_product_was = item.find('span', class_='was').find('span').text
            price_product_was = float(price_product_was[1:])

            price_product_now = item.find('span', class_='now').find('span').text
            price_product_now = float(price_product_now[1:])                    

            '''print('__________________________________')
            print(name_product+';','SKU:'+str(sku))
            print(domain_name+url_product)
            print('Was', price_product_was)
            print('Now', price_product_now)'''

            product = storage.Item(
                name_product, 
                sku, 
                domain_name + url_product, 
                price_product_was, 
                price_product_now)

            self.dict_product_items[product.sku] = product.__dict__
            '''Удачное ли решение вызвать костркутор одно класа внутри другого?
            Или лучше наследоваться? Но тогда вопрос, 
            можно ли отложить инциализацию родительского коструктора?'''
    
    def get_soup(self):
        return self.soup

    def get_dict_products(self):
        return self.dict_product_items

    def scrap(self):
        self._get_data(self.table_items)
        
def main():
    print(headers)
    count_from = 0
    scraper = Scraper()
    while response(url(count_from)) and find_not_found(scraper.get_soup()):
        # print(url())
        scraper.scrap()
        count_from += 204
        scraper.set_soup(count_from)
    jsons_wtiter.write_json(scraper.get_dict_products(), get_date())
    count_from = 0