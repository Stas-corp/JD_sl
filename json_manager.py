import check_products
import botinit
import check_page
import os
import telebot as tlb

bot = botinit.bot

class Manager:
    def __init__(self):
        self.onChouse_base: bool = False
        self.onChouse_second: bool = False
        self.base_json = str
        self.second_json = str
        self.json_list = [tuple] #(file, file_path)

    def _set_list_jsons(self):
        temp = []
        json_data_path = os.path.join('json_data')
        for file in os.listdir(json_data_path):
            if file.endswith('.json'): 
                temp.append((file, os.path.join(json_data_path, file)))

            if os.path.isdir(os.path.join(json_data_path, file)): 
                json_old_data_path = os.path.join(json_data_path, file)

                for file in os.listdir(json_old_data_path):
                    if file.endswith('.json'): 
                        temp.append((file, os.path.join(json_old_data_path, file)))        
        temp.sort()
        if temp != self.json_list:
            self.json_list = temp

    def _find_last_index(self, name_file: str):
        for num, file in enumerate(self.json_list):
            if name_file == file[0]:
                return num

    def set_base_json(self, name_file: str):
        self.base_json = name_file

    def set_second_json(self, name_file: str):
        self.second_json = name_file

    def chouse_base_file(self, mess: tlb.types.Message):
        self.onChouse_base = True
        self.onChouse_second = False
        self._set_list_jsons()
        message = f'Выбери первый файл который надо сравнить:'
        mrk = tlb.types.InlineKeyboardMarkup()
        for file, file_path in self.json_list:
            btn = tlb.types.InlineKeyboardButton(text=file, callback_data='first '+file)
            mrk.add(btn)
        bot.send_message(mess.chat.id, message, reply_markup=mrk)  

    def chouse_second_file(self, mess: tlb.types.Message):
        self.onChouse_base = False
        self.onChouse_second = True
        message = f'Выбери второй файл который надо сравнить:'
        mrk = tlb.types.InlineKeyboardMarkup()
        firs_index = self._find_last_index(self.base_json)
        for file, file_path in self.json_list[firs_index+1:]:
            btn = tlb.types.InlineKeyboardButton(text=file, callback_data='second '+file)
            mrk.add(btn)
        bot.send_message(mess.chat.id, message, reply_markup=mrk)

    def call_check_products(self, mess: tlb.types.Message):
        self.onChouse_base = False
        self.onChouse_second = False
        message = f'Выбраны два файла -> \nПервый: {self.base_json}\nВторой: {self.second_json}'
        mrk = tlb.types.InlineKeyboardMarkup()
        btn1 = tlb.types.InlineKeyboardButton('Сравнить выбранные файлы', callback_data='compare_select_jsons')
        mrk.add(btn1)
        bot.send_message(mess.chat.id, message, reply_markup=mrk)

if __name__ == '__main__':
    m = Manager()
    m._set_list_jsons()
    m._find_last_index(m.json_list[7][0])