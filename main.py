import storage
import requests
from bs4 import BeautifulSoup
import os
import io
import json
import arrow

directory_data = 'json_data'
date = arrow.now().format('YYMMDD,HH-mm-ss')
count_from = 0
dict_product_items = dict()
domain_name = 'https://www.global.jdsports.com'
headers = {
    'accept':'*/*',
    'user-agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36'
}
url = 'https://www.global.jdsports.com/men/brand/adidas-originals,nike,the-north-face,polo-ralph-lauren,jordan,champion,new-balance,napapijri/sale/?jd_sort_order=price-low-high&max=204'

def url():
    url = 'https://www.global.jdsports.com/men/brand/adidas-originals,nike,the-north-face,polo-ralph-lauren,jordan,champion,new-balance,napapijri/sale/?from='+str(count_from)+'&jd_sort_order=price-low-high&max=204' 
    return url

'''
def write_html():
    with open ('index.html', 'w', encoding='utf-8') as file:
        file.write(return_html(url).text)
        print('File writed!')

def read_html():
    try:
        with open('index.html', 'r', encoding='utf-8') as file:
            src = file.read()
            print('File read!')
            return src
    except (FileNotFoundError, EncodingWarning, EOFError, io.UnsupportedOperation) as exec:
        print(type(exec), 'Error reading index.html')'''

def find_not_found(page:BeautifulSoup):
    result = page.find('div', class_='not-found')
    if result == None:
        print('Page has a product')
        return True
    else:
        print('Page "404", process completed!')
        print(date)
        return False

def response(url):
    try:
        requests.get(url, headers=headers)
        print('Response received')
        return True
    except:
        print('No Response')
        return False

def return_html(url):
    src = requests.get(url, headers=headers)
    return src

def return_Soup():
    return BeautifulSoup(return_html(url()).text, 'lxml')


def change_json_name(path, new_file, was_file):
    file_path = os.path.join(path, new_file)
    if os.path.isfile(file_path):
        try:
            new_file_path = os.path.join(path, was_file)
            old_data_path = os.path.join(path,'old_dat')
            if not os.path.isdir(old_data_path):
                os.mkdir(old_data_path)
            if os.path.isfile(new_file_path):
                os.rename(new_file_path, os.path.join(old_data_path, date + '_' + was_file))
            os.rename(file_path, new_file_path)
        except Exception as e:
            print("ERROR! can't change filename!\n", e)
    else:
        print('No file to change')

def write_json(data = dict_product_items, path = directory_data, new_file = 'NEW_products.json', was_file = 'WAS_products.json'):
    if not os.path.isdir(path):
        os.mkdir(path)
    change_json_name(path, new_file, was_file)
    with open(path + '/' + new_file, 'w') as file:     
        json.dump(data, file)

def scrap():
    soup = return_Soup()

    table = soup.find('ul', class_='listProducts')
    
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
            name_product, sku, domain_name+url_product, price_product_was, price_product_now)

        dict_product_items[sku] = product.__dict__

def main():
    global count_from
    while response(url()) and find_not_found(return_Soup()):
        print(url())
        scrap()
        count_from += 204
    write_json()
        
if __name__ == "__main__":
    # write_html()
    main()