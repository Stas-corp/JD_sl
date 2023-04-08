import botinit
import check_products
import check_page
import call_parsser
import botinit
import task_manager
import json_manager

import time
import telebot as tlb

bot = botinit.bot
sch = botinit.sch
jsn = json_manager.Manager()
tsk = task_manager.Manager()

@bot.message_handler(commands=['start'])
def start(mess: tlb.types.Message):
    message = f'Hellow {mess.from_user.username},\nThis bot parsing site -> https://www.global.jdsports.com'
    bot.send_message(mess.chat.id, message, reply_markup=botinit.markup)

@bot.message_handler(commands=['check_page'])
def ss(mess: tlb.types.Message):
    check_page.check_page(mess)

@bot.message_handler(commands=['parsser'])
def parss(mess: tlb.types.Message):
    call_parsser.call_parsser(mess)

@bot.message_handler(content_types=['text'])
def reaction(mess: tlb.types.Message):
    if mess.text == botinit.button_pars.text:
        check_page.result_analyze(mess, check_page.send_set_sku)
        
    if mess.text == botinit.button_print_data.text:
        check_page.result_analyze(mess, check_page.send_single_sku)
        
    if mess.text == botinit.button_tasker_start.text:
        tsk.chouse_function(mess)

    if mess.text == botinit.button_tasker_remove.text:
        tsk.chouse_job(mess)

    if mess.text == botinit.button_chouse_json_file.text:
        jsn.chouse_base_file(mess)

    if mess.text == botinit.button_test.text:
        key = 'Message'
        message = ''
        message += f'<a href="http://www.coinmarketcap.com/">{key}</a>'
        bot.send_message(mess.chat.id, message, 'HTML')
        
@bot.callback_query_handler(func=lambda call:True)
def caller(call: tlb.types.CallbackQuery):

    '''if call.data == 'set_timout_parsser':
        input_timeout(call.message, call_parsser.set_new_timeout)

    if call.data == 'set_timeout_checker':
        input_timeout(call.message, check_page.set_timeout)'''
    
    if call.data == 'start_parss':
        parss(call.message)

    if tsk.onCreate:
        if call.data in [name_func for name_func in tsk.functions]:
            message = f'Вызванна функция: {call.data}'
            bot.send_message(call.message.chat.id, message)
            tsk.add_job(call.message, call.data)
    elif tsk.onDel:
        if call.data in [name_job for name_job in tsk.jobs]:
            tsk.remove_job(call.message, call.data)
            message = f'Удалена задача: {call.data}'
            bot.send_message(call.message.chat.id, message)
        else:
            message = f'Такой задачи нет или она уже удалена.'
            bot.send_message(call.message.chat.id, message)

    if jsn.onChouse_base:
        if call.data.startswith('first'):
            jsn.set_base_json(call.data.split(' ')[1])
            bot.delete_message(call.message.chat.id, call.message.id)
            jsn.chouse_second_file(call.message)
    elif jsn.onChouse_second:
        if call.data.startswith('second'):
            jsn.set_second_json(call.data.split(' ')[1])
            bot.delete_message(call.message.chat.id, call.message.id)
            jsn.call_check_products(call.message)
    
    if call.data == 'compare_select_jsons':
        check_page.result_analyze(call.message, check_page.send_set_sku, (jsn.base_json, jsn.second_json))

    bot.answer_callback_query(call.id)

'''def input_timeout(mess: tlb.types.Message, function):
    bot.delete_message(mess.chat.id, mess.message_id)
    message = f'Введите интервал (числом в минутах), с которым \будет собиратся новый список товаров:'
    bot.send_message(mess.chat.id, message)
    bot.register_next_step_handler(mess, function)'''

if __name__ == '__main__':
    sch.start()
    bot.get_updates()
    bot.polling(none_stop = True)
    # некст-степ webhook...