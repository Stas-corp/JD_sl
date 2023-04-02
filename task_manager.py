import call_parsser
import botinit
import check_page

import telebot as tlb

bot = botinit.bot
sch = botinit.sch

class Manager:
    def __init__(self):
        self.onCreate: bool = None
        self.jobs = {}
        self.functions = {
            'Parsser':call_parsser.call_parsser,
            'Checker Pg Item':check_page.check_page,
        }

    def chouse_function(self, mess: tlb.types.Message):
        message = f'Выбери функцию которую нужно запланировать:'
        mrk = tlb.types.InlineKeyboardMarkup()
        for name, func in self.functions.items():
            btn = tlb.types.InlineKeyboardButton(text=name, callback_data=name)
            mrk.add(btn)
        bot.send_message(mess.chat.id, message, reply_markup=mrk)

    def add_job(self, mess: tlb.types.Message, name_job):
        self.name_job = name_job
        bot.delete_message(mess.chat.id, mess.message_id)
        message = f'Добавление задачи: {name_job}\nУказать: интервал в минутах!'
        bot.send_message(mess.chat.id, message)
        bot.register_next_step_handler(mess, self._set_param_job)

    def _set_param_job(self, mess: tlb.types.Message):
        if mess.text.lower() != 'stop':
            try:
                timer = float(mess.text)
                self._creat_job(self.name_job, self.name_job, timer, mess)
                message = f'Задача: {self.name_job} создана!\nЗапуск через: {timer} минут(ы)'
                bot.send_message(mess.chat.id, message)
            except Exception as e:
                message = f"Не возможно установить таймер из-за ошибки:\n{e}\nПопробуйте снова или введите 'stop'."
                bot.send_message(mess.chat.id, message)
                bot.register_next_step_handler(mess, self._set_param_job)
        else:
            bot.send_message(mess.chat.id, 'Остановка ввода')

    def _creat_job(self, name_job:str, name_func, timer, *func_param):
        func = self.functions[name_func]
        j = sch.add_job(func, args=func_param, trigger='interval', minutes=timer, name=name_job)
        self.jobs[name_job] = j

    def chouse_job(self, mess: tlb.types.Message):
        message = f'Выбери задачу которая есть в планировщике:'
        mrk = tlb.types.InlineKeyboardMarkup()
        for name, job in self.jobs.items():
            btn = tlb.types.InlineKeyboardButton(text=name, callback_data=name)
            mrk.add(btn)
        bot.send_message(mess.chat.id, message, reply_markup=mrk)

    def remove_job(self, mess: tlb.types.Message, name_job):
        id = self.jobs[name_job].id
        sch.remove_job(id)
        self.jobs.pop(name_job)