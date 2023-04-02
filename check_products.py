import json

def _read_json(name):
    with open(name, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return dict(data)

def _read_data():
    actual_d = _read_json('json_data/NEW_products.json')
    was_d = _read_json('json_data/WAS_products.json')
    print('WAS Data len ->',len(was_d))
    print('NEW Data len ->',len(actual_d))
    return (actual_d, was_d)

'''def _check_actual_data(actual_data:dict, was_data:dict):
    temp_data = dict()
    for sku_new, data_new in actual_data.items():
        if sku_new in was_data:
            temp_data[sku_new] = was_data[sku_new]
    print('Temp Data len ->',len(temp_data))
    return temp_data

def _analyze_data(datas:tuple[dict]):
    actual_data, _ = datas
    filter_data = _check_actual_data(actual_data, _)
    new_data = dict()
    changed_price_data = dict()
    count = 0
    for sku_actual, data_actual in actual_data.items():
        if sku_actual in filter_data:
            if data_actual != filter_data[sku_actual]:
                print('Данные отличаются')
                print(data_actual)
                print('____________________')
                print(filter_data[sku_actual])
                if data_actual['price_now'] < filter_data[sku_actual]['price_now']:
                    print('Есть изменения цены')
                    changed_price_data[sku_actual] = data_actual
            else:
                print('Данные сходятся')
        else: # new product
            new_data[sku_actual] = data_actual 
    print ('Analyze completd')
    return {'New SKU':new_data,
            'Changed Price':changed_price_data}'''

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
    
def main():
    try:
        return _analyze_data(_read_data())
    except Exception as e:
        return f'ERORR read or analyze data from JSON!\nException -> {e}.'

if __name__ == '__main__':
    main()