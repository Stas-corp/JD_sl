import botinit
import check_products
import parsser
import callParsser

import telebot

import time
import arrow
import asyncio

bot = botinit.bot

markup = telebot.types.ReplyKeyboardMarkup(is_persistent=True, resize_keyboard=True)
button_pars = telebot.types.KeyboardButton('Print SKU')
button_print_data = telebot.types.KeyboardButton('Print Data')
button_test = telebot.types.KeyboardButton('Test')
button_set_timer = telebot.types.KeyboardButton('Set new timeout')

markup.add(
    button_pars, 
    button_print_data, 
    button_set_timer,
    button_test)

@bot.message_handler(commands=['start'])
def start(mess):
    message = f'Hellow {mess.from_user.username},\nThis bot parsing site -> https://www.global.jdsports.com'
    bot.send_message(mess.chat.id, message, reply_markup=markup)

@bot.message_handler(commands=['parsser'])
def parss(mess):
    callParsser.parss(mess)

@bot.message_handler(content_types='text')
def reaction(mess):
    if mess.text == button_pars.text:
        bot.send_message(mess.chat.id, 'Analyze processing...')
        list_new_sku = check_products.analyze_data()
        message = ''
        for key, dicts in list_new_sku.items():
            bot.send_message(mess.chat.id, key)
            for count, (sku, data) in enumerate(dicts.items()):
                if not count == len(dicts) - 1:
                    message += f'<a href="{data["url"]}">{str(sku)}</a>' + ', '
                    
                    if len(message.split(', ')) >= 20:
                        message += f'<a href="{data["url"]}">{str(sku)}</a>' + '.'
                        bot.send_message(mess.chat.id, message, 'HTML')
                        message = ''
                else:
                    message += f'<a href="{data["url"]}">{str(sku)}</a>' + '.'
            
            if not message:
                message = 'No data analyze!\nMessage is empty!'

            try:
                bot.send_message(mess.chat.id, message, 'HTML')
            except Exception as e:
                bot.send_message(mess.chat.id, 'Don`t send message, exception:\n'+str(e), 'HTML')
            message = ''

    if mess.text == button_print_data.text:
        bot.send_message(mess.chat.id, 'Analyze processing...')
        list_new_sku = check_products.analyze_data()
        for key, dicts in list_new_sku.items():
            bot.send_message(mess.chat.id, key)
            for count, (sku, data) in enumerate(dicts.items()):
                message = f'<a href="{data["url"]}">{str(sku)}</a>\n\
                Price WAS -> {data["price_was"]}\n\
                Price NOW -> {data["price_now"]}'
                bot.send_message(mess.chat.id, message, 'HTML')
                time.sleep(0.5)

    if mess.text == button_test.text:
        key = 'Message'
        message = ''
        message += f'<a href="http://www.coinmarketcap.com/">{key}</a>'
        bot.send_message(mess.chat.id, message, 'HTML')
        
    if mess.text == button_set_timer.text:
        message = f'Введите интервал (числом в минутах), с которым будет собиратся новый список товаров:'
        bot.send_message(mess.chat.id, message)
        bot.register_next_step_handler(mess, callParsser.set_new_timeout)

def get_now_time():
    return arrow.now().format('HH-mm-ss')

if __name__ == '__main__':
    bot.polling(none_stop = True)
    # некст-степ webhook...