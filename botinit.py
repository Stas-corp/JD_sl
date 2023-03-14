import telebot
import config
from apscheduler.schedulers.background import BackgroundScheduler
# правильно ли иницализацию сущности бота,
# делать подобным образом, в отдельном модуле?
# и как при этом делается вызов? один раз или он как-то кеширутся?
bot = telebot.TeleBot(config.TEST_TOKEN)
sch = BackgroundScheduler()