import telebot

markup = telebot.types.ReplyKeyboardMarkup(is_persistent=True, resize_keyboard=True)

button_pars = telebot.types.KeyboardButton('Print SKU')
button_print_data = telebot.types.KeyboardButton('Print Data')
button_test = telebot.types.KeyboardButton('Test')
button_set_timer = telebot.types.KeyboardButton('Set new timeout')
button_checker_start = telebot.types.KeyboardButton('Call checker')
button_checker_stop = telebot.types.KeyboardButton('STOP checker')

markup.add(
    button_pars, 
    button_print_data, 
    button_set_timer,
    button_checker_start,
    button_checker_stop,
    button_test)

