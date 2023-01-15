import storage
import requests
import lxml
from bs4 import BeautifulSoup
import io
import json
import arrow

data = arrow.now().format('YYMMDD,HH-mm-ss')
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

def find_not_found(page:BeautifulSoup):
    result = page.find('div', class_='not-found')
    if result == None:
        print('Page has a product')
        return True
    else:
        print('Page "404", process completed!')
        print(data)
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
        print(type(exec), 'Error reading index.html')

def write_json():
    with open(data +'_products.json', 'w') as file:     
        json.dump(dict_product_items, file)

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
    # нужна проверка перед перезаписью!
    write_json()
        
if __name__ == "__main__":
    # write_html()
    main()