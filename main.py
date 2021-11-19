import telebot
import config
from telebot import types
bot = telebot.TeleBot(config.TOKEN)

@bot.message_handler(commands=['start'])
def quickstart(message):
    bot.send_sticker(message.chat.id, "CAACAgIAAxkBAAEBxqpgBCLldd0_QYssYYNeFfTGgLaanwACWQEAAhAabSIdlWw5X85AHx4E")
    bot.send_message(message.chat.id, "Дорова епта бандиты")
    bot.send_message(message.chat.id, "Хочешь big cock?")
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button_phone = types.KeyboardButton(text="Yes, i waaaaaant")
    keyboard.add(button_phone)
    bot.send_message(message.chat.id,"Enter ypur age", reply_markup=keyboard)

@bot.message_handler(content_types=['text'])
def getMessage(message):
    #bot.send_message(message.chat.id, message)
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button_phone = types.KeyboardButton(text="Yes, i waaaaaant")
    keyboard.add(button_phone)
    bot.send_message(message.chat.id,
                     "Enter ypur age",
                     reply_markup=keyboard)


bot.polling(none_stop=True)
# def get_text_messages(message):
#     # Если написали «Привет»
#     if message.text == "Привет":
#         # Пишем приветствие
#         bot.send_message(message.from_user.id, "Привет, сейчас я расскажу тебе гороскоп на сегодня.")
#         # Готовим кнопки
#         keyboard = types.InlineKeyboardMarkup()
#         # По очереди готовим текст и обработчик для каждого знака зодиака
#         key_oven = types.InlineKeyboardButton(text='Овен', callback_data='zodiac')
#         # И добавляем кнопку на экран
#         keyboard.add(key_oven)
#         key_telec = types.InlineKeyboardButton(text='Телец', callback_data='zodiac')
#         keyboard.add(key_telec)
#         key_bliznecy = types.InlineKeyboardButton(text='Близнецы', callback_data='zodiac')
#         keyboard.add(key_bliznecy)
#         key_rak = types.InlineKeyboardButton(text='Рак', callback_data='zodiac')
#         keyboard.add(key_rak)
#         key_lev = types.InlineKeyboardButton(text='Лев', callback_data='zodiac')
#         keyboard.add(key_lev)
#         key_deva = types.InlineKeyboardButton(text='Дева', callback_data='zodiac')
#         keyboard.add(key_deva)
#         key_vesy = types.InlineKeyboardButton(text='Весы', callback_data='zodiac')
#         keyboard.add(key_vesy)
#         key_scorpion = types.InlineKeyboardButton(text='Скорпион', callback_data='zodiac')
#         keyboard.add(key_scorpion)
#         key_strelec = types.InlineKeyboardButton(text='Стрелец', callback_data='zodiac')
#         keyboard.add(key_strelec)
#         key_kozerog = types.InlineKeyboardButton(text='Козерог', callback_data='zodiac')
#         keyboard.add(key_kozerog)
#         key_vodoley = types.InlineKeyboardButton(text='Водолей', callback_data='zodiac')
#         keyboard.add(key_vodoley)
#         key_ryby = types.InlineKeyboardButton(text='Рыбы', callback_data='zodiac')
#         keyboard.add(key_ryby)
#         # Показываем все кнопки сразу и пишем сообщение о выборе
#         bot.send_message(message.from_user.id, text='Выбери свой знак зодиака', reply_markup=keyboard)
#     elif message.text == "/help":
#         bot.send_message(message.from_user.id, "Напиши Привет")
#     else:
#         bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help.")
# # Обработчик нажатий на кнопки
# @bot.callback_query_handler(func=lambda call: True)
# def callback_worker(call):
#     # Если нажали на одну из 12 кнопок — выводим гороскоп
#     if call.data == "zodiac":
#         # Формируем гороскоп
#         msg = random.choice(first) + ' ' + random.choice(second) + ' ' + random.choice(second_add) + ' ' + random.choice(third)
#         # Отправляем текст в Телеграм
#         bot.send_message(call.message.chat.id, msg)
# # Запускаем постоянный опрос бота в Телеграме
