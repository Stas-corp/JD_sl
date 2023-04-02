import botinit
import telebot as tlb
# import asyncio
# import check_products

bot = botinit.bot
prs = botinit.prs

task = None
timer_for_call_parsser = 0

def parss(mess: tlb.types.Message):
    if not timer_for_call_parsser:
        message = f'Таймер стоит на нуле, сбор не будет выполнятся, пока не будет установлен интервал'
        mrk = tlb.types.InlineKeyboardMarkup()
        button = tlb.types.InlineKeyboardButton(text='Установить таймер ⏱', callback_data='set_timout_parsser')
        mrk.add(button)
        bot.send_message(mess.chat.id, message, reply_markup=mrk)
    else:
        call_parsser(mess, timer_for_call_parsser)
        # asyncio.run(create_task(mess))

def set_new_timeout(mess: tlb.types.Message):
    global timer_for_call_parsser
    global task
    try:
        timer_for_call_parsser = float(mess.text)
        mrk = tlb.types.InlineKeyboardMarkup()
        button = tlb.types.InlineKeyboardButton(text='Запустить цикл сбора 📋', callback_data='start_parss')
        mrk.add(button)
        bot.send_message(mess.chat.id, f'Новый интервал установлен!', reply_markup=mrk)
        # if task and not task.done():
        #     stop_parsser(mess) 
    except Exception as e:
        message = f'Установка нового таймера не произошла из-из ошибки:\n{e}'
        bot.send_message(mess.chat.id, message)

def call_parsser(mess: tlb.types.Message, minutes:float = 0): # async
    # try:
        # while True:
    message = 'Начался сбор данных...\nПросьба не проводить аналитику!'
    bot.send_message(mess.chat.id, message, 'HTML')
    prs.main()
    bot.send_message(mess.chat.id, f'Сбор данных завершён!')
            # await asyncio.sleep(60 * minutes) # Только ради этого и нужен асинк....
    # except asyncio.CancelledError as e:
    #     pass

# def stop_parsser(mess):
#     global task
#     try:
#         task.cancel()
#         message = f'Цикл парсера остановлен!\nТребуется перезагрузка!'
#         bot.send_message(mess.chat.id, message)
#     except:
#         message = f'Цикл сбора не запущен!\nНечего останавливать!'
#         bot.send_message(mess.chat.id, message)
        
# async def create_task(mess):
#     global task
#     task = asyncio.create_task(call_parsser(mess, timer_for_call_parsser))
#     await task