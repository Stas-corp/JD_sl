import os
import json

def change_json_name(path:str, new_file:str, was_file:str, date:str):
    file_path = os.path.join(path, new_file)
    if os.path.isfile(file_path):
        try:
            new_file_path = os.path.join(path, was_file)
            old_data_path = os.path.join(path,'old_data')
            if not os.path.isdir(old_data_path):
                os.mkdir(old_data_path)
            if os.path.isfile(new_file_path):
                os.rename(new_file_path, os.path.join(old_data_path, f'{date}_{was_file}'))
            os.rename(file_path, new_file_path)
        except Exception as e:
            print(f"ERROR! can't change filename!\n{e}")
    else:
        print('No file to change')

def write_json(data:str, date:str, path = 'json_data', new_file = 'NEW_products.json', was_file = 'WAS_products.json'):
    if not os.path.isdir(path):
        os.mkdir(path)
    change_json_name(path, new_file, was_file, date)
    with open(f'{path}/{new_file}', 'w') as file: # was: path + '/' + new_file
        json.dump(data, file)