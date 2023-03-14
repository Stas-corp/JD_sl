import parsser
import botinit
import telebot
import check_products
import time

bot = botinit.bot
sch = botinit.sch

timer_schedule = 0

def check_page(mess):
    num_item_new = parsser.scraper.get_numder_items()
    num_item_last = len(check_products.get_data()[0])
    message = f'Сейчас на сайте {num_item_new} товаров.\nВ последнем сборе данных {num_item_last} товаров.'
    bot.send_message(mess.chat.id, message)

def creat_task(mess, timer):
    print(timer)
    sch.add_job(check_page, args=[mess], trigger='interval', minutes=timer, id='checker')

def stop_task(mess):
    try:
        sch.remove_job('checker')
    except:
        bot.send_message(mess.chat.id, 'Нет задач для отмены')
        
def set_timeout(mess):
    global timer_schedule
    try:
        timer_schedule = int(mess.text)
        mrk = telebot.types.InlineKeyboardMarkup()
        button = telebot.types.InlineKeyboardButton(text = 'Запустить задачу 📋', callback_data='check_page')
        mrk.add(button)
        bot.send_message(mess.chat.id, f'Новый интервал установлен!', reply_markup=mrk)
    except Exception as e:
        message = f'Установка нового таймера не произошла из-из ошибки:\n{e}'
        bot.send_message(mess.chat.id, message)
     
def main(mess):
    bot.send_message(mess.chat.id, f'Запуск планировщика проверки количества товаров.')
    if timer_schedule <= 0: 
        message = f'Значение timer_schedule -> {timer_schedule}.\nНужно установить таймер отправки сообщени про количество товаров.'
        mrk = telebot.types.InlineKeyboardMarkup()
        button = telebot.types.InlineKeyboardButton(text = 'Установить таймер ⏱', callback_data='set_timeout_checker')
        mrk.add(button)
        bot.send_message(mess.chat.id, message, reply_markup=mrk)
    else:
        creat_task(mess, timer_schedule)     