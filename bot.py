import botinit
import check_products
import check_page
import call_parsser
import botinit
import task_manager

import time
import telebot as tlb

bot = botinit.bot
sch = botinit.sch
tsk = task_manager.Manager()

@bot.message_handler(commands=['start'])
def start(mess: tlb.types.Message):
    message = f'Hellow {mess.from_user.username},\nThis bot parsing site -> https://www.global.jdsports.com'
    bot.send_message(mess.chat.id, message, reply_markup=botinit.markup)

@bot.message_handler(commands=['ss'])
def ss(mess: tlb.types.Message):
    check_page.check_page(mess)

@bot.message_handler(commands=['parsser'])
def parss(mess: tlb.types.Message):
    call_parsser.call_parsser(mess)

@bot.message_handler(content_types=['text'])
def reaction(mess: tlb.types.Message):
    if mess.text == botinit.button_pars.text:
        result_analyze(mess, send_set_sku)
        
    if mess.text == botinit.button_print_data.text:
        result_analyze(mess, send_single_sku)
        
    if mess.text == botinit.button_set_timer.text:
        input_timeout(mess, call_parsser.set_new_timeout)
        
    if mess.text == botinit.button_tasker_start.text:
        tsk.onCreate = True
        tsk.chouse_function(mess)

    if mess.text == botinit.button_tasker_remove.text:
        tsk.onCreate = False
        tsk.chouse_job(mess)

    if mess.text == botinit.button_test.text:
        key = 'Message'
        message = ''
        message += f'<a href="http://www.coinmarketcap.com/">{key}</a>'
        bot.send_message(mess.chat.id, message, 'HTML')
        
@bot.callback_query_handler(func=lambda call:True)
def caller(call: tlb.types.CallbackQuery):
    if call.data == 'set_timout_parsser':
        input_timeout(call.message, call_parsser.set_new_timeout)

    if call.data == 'set_timeout_checker':
        input_timeout(call.message, check_page.set_timeout)

    if call.data == 'start_parss':
        parss(call.message)

    if call.data == 'check_page':
        check_page.main(call.message)

    if tsk.onCreate:
        if call.data in [name_func for name_func in tsk.functions]:
            message = f'Вызванна функция: {call.data}'
            bot.send_message(call.message.chat.id, message)
            bot.answer_callback_query(call.id)
            tsk.add_job(call.message, call.data)

    else:
        if call.data in [name_job for name_job in tsk.jobs]:
            message = f'Удаляем задачу: {call.data}'
            bot.send_message(call.message.chat.id, message)
            bot.answer_callback_query(call.id)
            tsk.remove_job(call.message, call.data)

def input_timeout(mess: tlb.types.Message, function):
    bot.delete_message(mess.chat.id, mess.message_id)
    message = f'Введите интервал (числом в минутах), с которым \будет собиратся новый список товаров:'
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

def result_analyze(mess: tlb.types.Message, function):
    datas = check_products.main()
    if isinstance(datas, dict):
        function(mess, datas)
    else:
        bot.send_message(mess.chat.id, datas)

if __name__ == '__main__':
    sch.start()
    bot.get_updates()
    bot.polling(none_stop = True)
    # некст-степ webhook...