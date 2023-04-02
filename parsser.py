import storage
import jsons_wtiter

import requests
from bs4 import BeautifulSoup
from fake_headers import Headers

import io
import arrow

domain_name = 'https://www.global.jdsports.com'
headers = Headers(headers=True).generate()

def get_date():
    return arrow.now().format('YYMMDD,HH-mm-ss')

def write_html(page):
    with open('index.html', 'w', encoding='utf-8') as file:
        file.write(page)

class Scraper:
    def __init__(self):
        self.soup = None
        self.table_items = None
        self.number_items = None
        self.dict_product_items = dict()
        self.url = None
        self.set_soup() # правильно ли, вызывать метод в кострукторе, который иницализирует поле?  

    def set_url(self, count_from: int):
        self.url = f'https://www.global.jdsports.com/men/brand/adidas-originals,nike,the-north-face,polo-ralph-lauren,jordan,champion,new-balance,napapijri/sale/?from={count_from}&jd_sort_order=price-low-high&max=204'

    def _search_data(self, table: set[BeautifulSoup]):
        for item in table:
            if item.find('span', class_="was") != None and item.find('span', class_="pri") != None:
                # print('\n',item,'\n')
                name_product = item.find('span', class_='itemTitle').text.replace('\n','')
                sku = item.find('span', class_='itemContainer').get('data-productsku')
                url_product = item.find('span', class_='itemTitle').find('a').get('href')
                
                price_product_was = item.find('span', class_='was').find('span').text
                price_product_was = float(price_product_was[1:])

                price_product_now = item.find('span', class_='now').find('span').text
                price_product_now = float(price_product_now[1:])

                product = storage.Item(
                name_product, 
                sku, 
                domain_name + url_product, 
                price_product_was, 
                price_product_now)

                self.dict_product_items[product.sku] = product.__dict__
            else:
                print(domain_name + item.find('span', class_='itemTitle').find('a').get('href')) 

            '''print('__________________________________')
            print(name_product+';','SKU:'+str(sku))
            print(domain_name + url_product)
            print('Was', price_product_was)
            print('Now', price_product_now)'''
 
        print(len(self.dict_product_items))
        '''Удачное ли решение вызвать костркутор одно класа внутри другого?
        Или лучше наследоваться? Но тогда вопрос, 
        можно ли отложить инциализацию родительского коструктора?'''

    def _request(self, count_from):
        self.set_url(count_from)
        return requests.get(self.url, headers=headers).text

    def set_soup(self, count_from = 0):
        self.soup = BeautifulSoup(self._request(count_from), 'lxml')

    def get_numder_items(self):
        self.set_soup()
        self.number_items = int(self.soup.find('div', class_='pageCount').text.strip().split(' ')[0])
        return self.number_items
        
    def get_soup(self):
        return self.soup

    def get_dict_products(self):
        return self.dict_product_items

    def scrap(self):
        self.table_items = self.soup.find('ul', class_='listProducts').find_all('li', class_='productListItem')
        self._search_data(self.table_items)

    def main(self):
        count_from = 0
        while response(self.url) and find_not_found(self.get_soup()):
            self.scrap()
            count_from += 204
            self.set_soup(count_from)
        jsons_wtiter.write_json(self.get_dict_products(), get_date())

def find_not_found(page: BeautifulSoup):
    result = page.find('div', class_='not-found')
    if result == None:
        print('Page has a product')
        return True
    else:
        print('Page "404", process completed!')
        print(get_date())
        return False

def response(url: str):
    try:
        requests.get(url, headers=headers)
        print('Response received')
        return True
    except:
        print('No Response')
        return False

if __name__ == "__main__":
    scraper = Scraper()
    scraper.main()