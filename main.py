import telebot
import config
import database
import json
from telebot import types
#import registration # registration module
from user import User  # user definition
from database import *

user_dict = {}
DATA_JSON = "data.json"
bot = telebot.TeleBot(config.TOKEN)

""" start command processing """
"""@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEDUrphmCOr4kukL99zoy9Vop4nguUGqgACQAADOPCiGncMZgcCUVNuIgQ')
    bot.send_message(message.chat.id,'Привет, хочешь знакомиться?')
    markup = types.ReplyKeyboardMarkup(True, True)
    markup.add(types.KeyboardButton("Да, я хочу знакомств"))
    markup.add(types.KeyboardButton("Нет, я хочу уйти"))
    bot.send_message(message.chat.id, 'Выберите что вам надо', reply_markup=markup)
    #markup.editMessageReplyMarkup(reply_markup=1)"""

""" text command processing """
"""
@bot.message_handler(content_types='text')
def message_reply(message):
    if message.text=="Да, я хочу знакомств":
        msg = bot.reply_to(message, "Введите свой возраст")
        bot.register_next_step_handler(msg, process_age_step)
    elif message.text=="Нет, я хочу уйти":
        bot.send_message(message.chat.id,'Спасибо использование бота!')
        #bot.stop_polling()
    else:
        bot.send_message(message.chat.id, 'Пожалуйста повторите запрос!')
def process_age_step(message):
    try:
        chat_id = message.chat.id
        age = message.text
        user = User(message.from_user.username, int(age))
        user_dict[chat_id] = str(user)
        msg = bot.reply_to(message, 'Я тебя понял, на этом всё, последние слова?')
        bot.register_next_step_handler(msg, process_dumb_step)
    except Exception as e:
        print(e)
        bot.reply_to(message, 'Что-то не так, попробуй еще раз')
def process_dumb_step(message):
    with open(DATA_JSON, "w") as f:
        json.dump(user_dict, f, indent = 4)
    #bot.stop_polling()
    #pass
@bot.message_handler(commands=['stop'])
def stop_auth(message):
    bot.stop_polling()
    pass
bot.polling(none_stop=True, interval=0)
"""


@bot.message_handler(commands=['start'])  # начинаем
def start(message):
    bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEDUrphmCOr4kukL99zoy9Vop4nguUGqgACQAADOPCiGncMZgcCUVNuIgQ')

    markup_start_choice = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2,
                                                    one_time_keyboard=True)  # задали формат кнопок
    yesbutton = types.KeyboardButton("Yes, i want")
    nobutton = types.KeyboardButton("No, i won't")
    markup_start_choice.add(yesbutton, nobutton)  # добавили кнопки

    bot.send_message(message.chat.id, "Привет, начнем?",
                     reply_markup=markup_start_choice)  # подвязали кнопки к сообщению


# @bot.callback_query_handler(func=lambda call: True)
# def answer(call):
#     if call.data == "Yes, i want":
#         bot.send_message(call.message.chat.id, "halo")
#
#     elif call.data == 'no':
#         pass

@bot.message_handler(content_types=['text'])  # обрабатываем кнопки клавиатуры
def getText(message):
    if message.text == 'Yes, i want':  # c кнопки старта переходим в меню
        menu(message)
    elif message.text == "No, i won't":
        bot.send_message(message.chat.id, "exit")  # доделать
        backMenu(message)
    elif message.text == '1':  # create profile
        user_profile(message) # from registration module
    elif message.text == 'Menu':
        menu(message)

    # types.ReplyKeyboardRemove()
    # bot.send_message(message.chat.id, 'Hello')
    # markup = types.ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True, row_width=2)
    # btn0 = types.KeyboardButton("Мой профиль")
    # btn1 = types.KeyboardButton("Настройки поиска")
    # btn2 = types.KeyboardButton("Ищем любовь")
    # btn3 = types.KeyboardButton("Кому я нравлюсь")
    # btn4 = types.KeyboardButton("Копейка в развитие")
    # markup.add(btn0, btn1, btn2, btn3, btn4)
    # bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEDUrphmCOr4kukL99zoy9Vop4nguUGqgACQAADOPCiGncMZgcCUVNuIgQ')
    # start_handler = f"<b>Что дальше, {message.from_user.first_name}?</b>"
    # msg = bot.send_message(message.chat.id, start_handler, parse_mode='html', reply_markup=markup)
    # bot.register_next_step_handler(msg, menu_next)


""" regular menu """

def menu(message):
    markup_menu = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3, one_time_keyboard=True)
    profilebutton = types.KeyboardButton("1")
    viewbutton = types.KeyboardButton("2")
    stopbutton = types.KeyboardButton("3")
    markup_menu.add(profilebutton, viewbutton, stopbutton)
    bot.send_message(message.chat.id, f"1. My profile\n"
                                      f"2. View profile\n"
                                      f"3. Stop",
                     reply_markup=markup_menu)


""" Menu after u don't want continue"""

def backMenu(message):
    markup_back = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1,
                                            one_time_keyboard=True)  # задали формат кнопок
    backbutton = types.KeyboardButton("Menu")

    markup_back.add(backbutton)  # добавили кнопки

    bot.send_message(message.chat.id, "hope u find a friend",
                     reply_markup=markup_back)  # подвязали кнопки к сообщению


# def profile_next(message):
#     get_message_bot = message.text
#     markup = types.ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True, row_width=2)
#     btn0 = types.KeyboardButton("Мой профиль")
#     btn1 = types.KeyboardButton("Настройки поиска")
#     btn2 = types.KeyboardButton("Ищем любовь")
#     btn3 = types.KeyboardButton("Кому я нравлюсь")
#     btn4 = types.KeyboardButton("Копейка в развитие")
#     markup.add(btn0, btn1, btn2, btn3, btn4)
#     bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEDUrphmCOr4kukL99zoy9Vop4nguUGqgACQAADOPCiGncMZgcCUVNuIgQ')
#     start_handler = f"<b>Что дальше, {message.from_user.first_name}?</b>"
#     msg = bot.send_message(message.chat.id, start_handler, parse_mode='html', reply_markup=markup)
#
#     if get_message_bot == "Заполнить профиль":
#         bot.send_message(message.chat.id, "Ребят тут делаем заполнение аккаунта", parse_mode='html')
#         # user_profile(message)
#         bot.register_next_step_handler(msg, menu_next)
#     elif get_message_bot == "Удалить профиль":
#         bot.send_message(message.chat.id, "Удалил профиль", parse_mode='html')
#         bot.register_next_step_handler(msg, menu_next)
#     elif get_message_bot == "Главное меню":
#         bot.send_message(message.chat.id, "Главное меню", parse_mode='html')
#         bot.register_next_step_handler(msg, menu_next)
#     else:
#         bot.send_message(message.chat.id, "Неправильный ввод", parse_mode='html')
#         bot.register_next_step_handler(message, profile_next)

def user_profile(message):
    name = bot.send_message(message.chat.id, 'Введи имя')
    bot.register_next_step_handler(name, process_name_step)


def process_name_step(message):
    try:
        chatID = message.chat.id
        name = message.text

        user_dict['chatID'] = chatID
        user_dict['name'] = name

        msg = bot.send_message(message.chat.id, 'How old are you?')
        bot.register_next_step_handler(msg, process_age_step)
    except Exception as e:
        bot.reply_to(message, 'oops')


def process_age_step(message):
    try:
        age = message.text
        if not age.isdigit():
            msg = bot.send_message(message.chat.id, 'Age should be a number. How old are you?')
            bot.register_next_step_handler(msg, process_age_step)
            return

        # user = user_dict[chatID]
        # user.age = age
        user_dict['age'] = age

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2, one_time_keyboard=True)
        markup.add('Male', 'Female')
        msg = bot.send_message(message.chat.id, 'What is your gender', reply_markup=markup)
        bot.register_next_step_handler(msg, process_sex_step)
    except Exception as e:
        bot.reply_to(message, 'oooops')


def process_sex_step(message):
    try:
        sex = message.text

        user = User(user_dict['chatID'], user_dict['name'])

        user_dict['sex'] = sex
        user.age = user_dict['age']
        user.sex = user_dict['sex']

        if (sex == u'Male') or (sex == u'Female'):
            print(user_dict)
            print(user)
            pass
        else:
            raise Exception("Unknown sex")

        writing(user)
        bot.send_message(user_dict['chatID'],
                         'Nice to meet you, ' + user.name + '\n Age: ' + str(user.age) + '\n Sex: ' + user.sex)
    except Exception as e:
        bot.reply_to(message, 'oooops')



if __name__ == '__main__':
    bot.polling(none_stop=True)

bot.polling(none_stop=True)
