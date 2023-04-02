import check_products
import botinit

import os
import telebot as tlb

class Manager:
    def __init__(self):
        self.base_json = None
        self.modified_json = None
        self.json_list = []

    def set_list_jsons(self):
        json_data_path = os.path.join('json_data')

        for file in os.listdir(json_data_path):
            if file.endswith('.json'): 
                self.json_list.append(file)

            if os.path.isdir(os.path.join(json_data_path, file)): 
                json_old_data_path = os.path.join(json_data_path, file)

                for file in os.listdir(json_old_data_path):
                    if file.endswith('.json'): 
                        self.json_list.append(file)
                
        self.json_list.sort()
        for file in self.json_list:
            print(file)
        

if __name__ == '__main__':
    m = Manager()
    m.set_list_jsons()
    print(type(m))
