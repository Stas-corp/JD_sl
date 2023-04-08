import json

def _read_json(name):
    with open(name, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return dict(data)

def _read_data(base, second):
    actual_d = _read_json(base)
    was_d = _read_json(second)
    print('WAS Data len ->',len(was_d))
    print('NEW Data len ->',len(actual_d))
    return (actual_d, was_d)

def _analyze_data(datas: tuple[dict]):
    new_products = dict()
    price_changes = dict()
    for sku, product1 in datas[0].items():
        product2 = datas[1].get(sku)
        if product2 is None:
            new_products[sku] = product1
        elif product1['price_now'] < product2['price_now']:
            price_changes[sku] = product1
            price_changes[sku]['price_was'] = product2['price_now']
    return {'New SKU':new_products,
            'Changed Price': price_changes}

def get_data():
    '''-> tuple ( 'dict actual_data' , 'dict was_data' )'''
    actual_d = _read_json('json_data/NEW_products.json')
    was_d = _read_json('json_data/WAS_products.json')
    return (actual_d, was_d)
    
def main(names=('json_data/NEW_products.json','json_data/WAS_products.json')):
    try:
        return _analyze_data(_read_data(names[0], names[1]))
    except Exception as e:
        return f'ERORR read or analyze data from JSON!\nException -> {e}.'

if __name__ == '__main__':
    main()