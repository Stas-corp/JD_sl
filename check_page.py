import botinit
import check_products
import call_parsser

import telebot as tlb
import time

bot = botinit.bot
sch = botinit.sch
prs = botinit.prs

timer_schedule = 0

def check_page(mess: tlb.types.Message):
    num_item_new = prs.get_numder_items()
    num_item_last = len(check_products.get_data()[0])
    message = f'Сейчас на сайте {num_item_new} товаров.\nВ последнем сборе данных {num_item_last} товаров.'
    bot.send_message(mess.chat.id, message)
    if num_item_last != num_item_new:
        call_parsser.call_parsser(mess)

def send_set_sku(mess: tlb.types.Message, datas: dict):
    bot.send_message(mess.chat.id, 'Analyze processing...')
    for key, dicts in datas.items():
        message = ''
        bot.send_message(mess.chat.id, key)
        for count, (sku, data) in enumerate(dicts.items()):
            if not count == len(dicts) - 1:
                message += f'<a href="{data["url"]}">{str(sku)}</a>, ' 
                if len(message.split(', ')) >= 40:
                    message += f'<a href="{data["url"]}">{str(sku)}</a>.'
                    bot.send_message(mess.chat.id, message, 'HTML')
                    message = ''
            else:
                message += f'<a href="{data["url"]}">{str(sku)}</a>.'
        if not message:
            message = 'No data analyze!\nMessage is empty!'
        try:
            bot.send_message(mess.chat.id, message, 'HTML')
        except Exception as e:
            bot.send_message(mess.chat.id, 'Don`t send message, exception:\n'+str(e), 'HTML')

def send_single_sku(mess: tlb.types.Message, datas: dict):
    bot.send_message(mess.chat.id, 'Analyze processing...')
    for key, dicts in datas.items():
        bot.send_message(mess.chat.id, key)
        for count, (sku, data) in enumerate(dicts.items()):
            if key == 'Changed Price':
                message = f'<a href="{data["url"]}">{str(sku)}</a>\n\
                Price OLD -> {data["price_was"]}\n\
                Price NEW -> {data["price_now"]}'
            else:
                message = f'<a href="{data["url"]}">{str(sku)}</a>\n\
                Price WAS -> {data["price_was"]}\n\
                Price NOW -> {data["price_now"]}'
            bot.send_message(mess.chat.id, message, 'HTML')
            time.sleep(0.1)

def result_analyze(mess: tlb.types.Message, function, *args):
    datas = check_products.main(*args)
    if isinstance(datas, dict):
        function(mess, datas)
    else:
        bot.send_message(mess.chat.id, datas)

if __name__ == '__main__':
    pass