import storage
import requests
import lxml
from bs4 import BeautifulSoup
import io
import json
import time

count_from = 0
dict_product_items = dict()
domain_name = 'https://www.global.jdsports.com'
headers = {
    'accept':'*/*',
    'user-agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36'
}
url = 'https://www.global.jdsports.com/men/brand/adidas-originals,nike,the-north-face,polo-ralph-lauren,jordan,champion,new-balance,napapijri/sale/?from=0&jd_sort_order=price-low-high'

def url():
    url = 'https://www.global.jdsports.com/men/brand/adidas-originals,nike,the-north-face,polo-ralph-lauren,jordan,champion,new-balance,napapijri/sale/?from='+str(count_from)+'&jd_sort_order=price-low-high' 
    return url

def response(url):
    try:
        requests.get(url, headers=headers)
        print('Response received')
        return True
    except:
        print('No Response')
        return False

def get_html(url):
    src = requests.get(url, headers=headers)
    return src

def write_html():
    with open ('index.html', 'w', encoding='utf-8') as file:
        file.write(get_html(url).text)
        print('File writed!')

def write_json():
    with open('products.json', 'w') as file:     
        json.dump(dict_product_items, file)

def read_html():
    try:
        with open('index.html', 'r', encoding='utf-8') as file:
            src = file.read()
            print('File read!')
            return src
    except (FileNotFoundError, EncodingWarning, EOFError, io.UnsupportedOperation) as exec:
        print(type(exec), 'Error reading index.html')

def scrap():
    print(url())
    soup = BeautifulSoup(get_html(url()).text, 'lxml')

    # находим таблицу с карточками товара
    table = soup.find('ul', class_='listProducts')
    # создаём список из элементов таблицы
    table_items = list(table.find_all('li', class_='productListItem')) 

    for item in table_items:
        print('__________________________________')
        name_product = item.find('span', class_='itemTitle').text.replace('\n','')
        sku = item.find('span', class_='itemContainer').get('data-productsku')
        print(name_product+';','SKU:'+str(sku))

        url_product = item.find('span', class_='itemTitle').find('a').get('href')
        print(domain_name+url_product)

        price_product_was = item.find(
            'span', class_='was').find('span').text
        print('Was', price_product_was)
        price_product_was = float(price_product_was[1:])

        price_product_now = item.find(
            'span', class_='now').find('span').text
        print('Now', price_product_now)
        price_product_now = float(price_product_now[1:])

        product = storage.Item(
            name_product, sku, url_product, price_product_was, price_product_now)
        dict_product_items[sku] = product.__dict__

def main():
    while response(url()):
        

if __name__ == "__main__":
    # write_html()
    scrap()