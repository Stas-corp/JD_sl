import json

asd = []

def read_json(name):
    with open(name, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data

was_d = dict(read_json('NEWproducts.json'))
actual_d = dict(read_json('230115,13-41-01_products.json'))

print('WAS Data len ->',len(was_d))
print('NEW Data len ->',len(actual_d))

def check_actual_data(actual_data:dict, was_data:dict):
    '''Проверяет старые данные и новые на вхождение.
    Возвращает словарь данных, которые сошлись.'''
    temp_data = dict()
    for sku_new, data_new in actual_data.items():
        if sku_new in was_data:
            temp_data[sku_new] = was_data[sku_new]
    '''
    count = 0
    for sku in temp_data.keys():
        if not temp_data[sku] == was_data[sku] == actual_data[sku]:
            print(sku, 'ATTENTION!!! Data inconsistency')
            count+=1 
    print('Data with changes ->', count)
    '''     
    print('Temp Data len ->',len(temp_data))
    return temp_data

def analyze_data(actual_data:dict=actual_d):
    filter_data = check_actual_data(actual_d, was_d)
    new_sku = list()
    changed_price_sku = list()
    count = 0
    for sku_actual, data_actual in actual_data.items():
        if sku_actual in filter_data:
            if data_actual == filter_data[sku_actual]:
                # print(sku_actual, 'Without change...')
                pass
            else:
                # print(sku_actual, 'Сhanges FOUND!')
                count += 1
                if data_actual['price_now'] < filter_data[sku_actual]['price_now']:
                    # print('^^^^^^ CHANGE PRICE!!!')
                    # print('Price WAS ->', filter_data[sku_actual]['price_now'])
                    # print('Print NOW ->', data_actual['price_now'])
                    changed_price_sku.append(sku_actual)
        else:
            # print(sku_actual, 'NEW PRODUCT!!!')
            new_sku.append(sku_actual)
    # print('New SKU ->', new_sku)
    # print('Data with changes ->', count)
    return new_sku

analyze_data(actual_d)