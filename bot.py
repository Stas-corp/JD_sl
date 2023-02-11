import config
import telebot
import check_products

bot = telebot.TeleBot(config.TOKEN)

@bot.message_handler(commands=['start'])
def start(messege):
    mess = f'Hellow {messege.from_user.username},\nThis bot parsing site -> https://www.global.jdsports.com'
    markup = telebot.types.ReplyKeyboardMarkup(is_persistent=True, resize_keyboard=True)
    button1 = telebot.types.KeyboardButton('Parsing')
    button2 = telebot.types.KeyboardButton('Test')
    markup.add(button1)
    markup.add(button2)
    bot.send_message(messege.chat.id, mess, reply_markup=markup)

@bot.message_handler(content_types='text')
def parsing(messege):
    if messege.text == 'Parsing':
        bot.send_message(messege.chat.id, 'Analyze processing...')
        list_new_sku = check_products.analyze_data()
        message = ''
        for key, dicts in list_new_sku.items():
            bot.send_message(messege.chat.id, key)
            for count, (sku, data) in enumerate(dicts.items()):
                if not count == len(dicts) - 1:
                    message += f'<a href="{data["url"]}">{str(sku)}</a>' + ', '
                    
                    if len(message.split(', ')) >= 20:
                        message += f'<a href="{data["url"]}">{str(sku)}</a>' + '.'
                        bot.send_message(messege.chat.id, message, 'HTML')
                        message = ''
                else:
                    message += f'<a href="{data["url"]}">{str(sku)}</a>' + '.'

            bot.send_message(messege.chat.id, message, 'HTML')
            message = ''

    if messege.text == 'Test':
        key = 'Message'
        message = ''
        message += f'<a href="http://www.coinmarketcap.com/">{key}</a>'
        bot.send_message(messege.chat.id, message, 'HTML')
        print('test')

bot.polling(none_stop = True)

'''
1. вывод актуальной инфы.
2. real-time
3. 

'''