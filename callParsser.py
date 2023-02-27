import parsser
import botinit
import asyncio

bot = botinit.bot

task = None
timer_for_call_parsser = 0

def parss(mess):
    if not timer_for_call_parsser:
        message = f'Таймер стоит на нуле, сбор не будет выполнятся, пока не будет установлен интервал'
        bot.send_message(mess.chat.id, message)
    else:
        asyncio.run(async_main(mess))

def set_new_timeout(mess):
    global timer_for_call_parsser
    global task
    try:
        timer_for_call_parsser = float(mess.text)
        message = f'Новый интервал установлен!'
        bot.send_message(mess.chat.id, message)
        if task and not task.done():
            task.cancel()
            message = f'Цикл парсера остановлен!\nТребуется перезагрузка!'
            bot.send_message(mess.chat.id, message)
    except Exception as e:
        message = f'Установка нового таймера не произошла из-из ошибки:\n{e}\nСкорее всего было введено не число'
        bot.send_message(mess.chat.id, message)

async def call_parsser(mess, minutes:float):
    try:
        while True:
            message = "Начался сбор данных...\nПросьба не проводить аналитику!"
            bot.send_message(mess.chat.id, message, 'HTML')
            parsser.main()
            message = f"Сбор данных завершён!\nСледующий сбор будет через {minutes} минут."
            bot.send_message(mess.chat.id, message, 'HTML')
            # Только ради этого и нужен асинк....
            await asyncio.sleep(60 * minutes)

    except asyncio.CancelledError:
        message = f"Прерывание функции CancelledError, цикл сбора данных остановлен."
        bot.send_message(mess.chat.id, message, 'HTML')

async def async_main(mess):
    global task
    task = asyncio.create_task(call_parsser(mess, timer_for_call_parsser))
    await task