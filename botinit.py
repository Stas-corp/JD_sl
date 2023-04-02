import config
import parsser
import telebot
from apscheduler.schedulers.background import BackgroundScheduler
# правильно ли иницализацию сущности бота,
# делать подобным образом, в отдельном модуле?
# и как при этом делается вызов? один раз или он как-то кеширутся?
bot = telebot.TeleBot(config.TEST_TOKEN)
sch = BackgroundScheduler()
prs = parsser.Scraper()

markup = telebot.types.ReplyKeyboardMarkup(is_persistent=True, resize_keyboard=True)

button_pars = telebot.types.KeyboardButton('Print SKU')
button_print_data = telebot.types.KeyboardButton('Print Data')
button_test = telebot.types.KeyboardButton('Test')
button_set_timer = telebot.types.KeyboardButton('Set new timeout')
button_tasker_start = telebot.types.KeyboardButton('Create TASK')
button_tasker_remove = telebot.types.KeyboardButton('Stop TASK')

markup.add(
    button_pars, 
    button_print_data, 
    button_tasker_start,
    button_tasker_remove,
    button_test)