import botinit
import check_products
import check_page
import call_parsser
import markup

import telebot as tlb

import time
import arrow
import asyncio

bot = botinit.bot
sch = botinit.sch

@bot.message_handler(commands=['start'])
def start(mess: tlb.types.Message):
    message = f'Hellow {mess.from_user.username},\nThis bot parsing site -> https://www.global.jdsports.com'
    bot.send_message(mess.chat.id, message, reply_markup=markup.markup)

@bot.message_handler(commands=['parsser'])
def parss(mess):
    call_parsser.parss(mess)

@bot.message_handler(commands=['stop'])
def stop_pars(mess):
    call_parsser.stop_parsser(mess)

@bot.message_handler(content_types=['text'])
def reaction(mess: tlb.types.Message):
    if mess.text == markup.button_pars.text:
        result_analyze(mess, send_set_sku)
        
    if mess.text == markup.button_print_data.text:
        result_analyze(mess, send_single_sku)
        
    if mess.text == markup.button_set_timer.text:
        input_timeout(mess, call_parsser.set_new_timeout)
        
    if mess.text == markup.button_checker_start.text:
        check_page.main(mess)

    if mess.text == markup.button_checker_stop.text:
        check_page.stop_task(mess, )

    if mess.text == markup.button_test.text:
        key = 'Message'
        message = ''
        message += f'<a href="http://www.coinmarketcap.com/">{key}</a>'
        bot.send_message(mess.chat.id, message, 'HTML')
        
@bot.callback_query_handler(func=lambda call:True)
def set_timout(call: tlb.types.CallbackQuery):
    if call.data == 'set_timout_parsser':
        input_timeout(call.message, call_parsser.set_new_timeout)

    if call.data == 'set_timeout_checker':
        input_timeout(call.message, check_page.set_timeout)

    if call.data == 'start_parss':
        parss(call.message)

    if call.data == 'check_page':
        check_page.main(call.message)

def input_timeout(mess, function):
    bot.delete_message(mess.chat.id, mess.message_id)
    message = f'Введите интервал (числом в минутах), с которым будет собиратся новый список товаров:'
    bot.send_message(mess.chat.id, message)
    bot.register_next_step_handler(mess, function)

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
            message = f'<a href="{data["url"]}">{str(sku)}</a>\n\
            Price WAS -> {data["price_was"]}\n\
            Price NOW -> {data["price_now"]}'
            bot.send_message(mess.chat.id, message, 'HTML')
            time.sleep(0.5)

def result_analyze(mess: tlb.types.Message, function):
    datas = check_products.main()
    print(datas, type(datas))
    if isinstance(datas, dict):
        function(mess, datas)
    else:
        bot.send_message(mess.chat.id, datas)

if __name__ == '__main__':
    sch.start()
    bot.polling(none_stop = True)
    # некст-степ webhook...