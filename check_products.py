import json

def read_json(name):
    with open(name, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data

was_d = read_json('productsW.json')
new_d = read_json('products.json')

print('WAS Data len ->',len(was_d))
print('NEW Data len ->',len(new_d))

def check_actual_data(new:dict, was:dict):
    count = 1
    temp_data = dict()
    for sku_n, data_n in new.items():
        if sku_n in was:
            print(sku_n, data_n)
            temp_data[sku_n] = data_n
            print(count)
            count+=1

#check_actual_data(new_d, was_d)


