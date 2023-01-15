import config
import telebot
import check_products

def test():
    print('test')

bot = telebot.TeleBot(config.TOKEN)

@bot.message_handler(commands=['start'])
def start(messege):
    mess = f'Hellow {messege.from_user.username},\nThis bot parsing site -> https://www.global.jdsports.com'
    markup = telebot.types.ReplyKeyboardMarkup(is_persistent=True, resize_keyboard=True)
    button1 = telebot.types.KeyboardButton('Parsing')
    markup.add(button1)
    bot.send_message(messege.chat.id, mess, reply_markup=markup)

@bot.message_handler()
def parsing(messege):
    if messege.text == 'Parsing':
        bot.send_message(messege.chat.id, 'Analyze processing...')
        list_new_sku = check_products.analyze_data()
        for item in list_new_sku:
            bot.send_message(messege.chat.id, item)

bot.polling(none_stop = True)