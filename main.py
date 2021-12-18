from batya import bot
from telebot import types
#import registration # registration module
from userRegistration import UserRegistration
from database import *

#user_dict = {}
DATA_JSON = "data.json"


@bot.message_handler(commands=['start'])  # начинаем
def start(message):
    print(message.chat.id)
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
        menustarter(message)
    elif message.text == "No, i won't":
        bot.send_message(message.chat.id, "exit")  # доделать
        backMenu(message)
    elif message.text == 'Create profile':  # create profile
        registration = UserRegistration()
        registration.create_user(message)# from registration module
    elif message.text == 'Menu':
        menustarter(message)


#@bot.message_handler(content_types= ['photo'])

""" regular menu """
def menustarter(message):
    if checkuser(message.chat.username):
        loggedmenu(message)
    else:
        guestmenu(message)
def guestmenu(message):
    markup_menu = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3, one_time_keyboard=True)
    profilebutton = types.KeyboardButton("Create profile")
    stopbutton = types.KeyboardButton("Stop")
    markup_menu.add(profilebutton, stopbutton)
    bot.send_message(message.chat.id, f"Choose your option",
                     reply_markup=markup_menu)
def loggedmenu(message):
    markup_menu = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3, one_time_keyboard=True)
    startbutton = types.KeyboardButton("Start")
    editbutton = types.KeyboardButton("Edit my profile")
    stopbutton = types.KeyboardButton("Stop")
    markup_menu.add(startbutton, editbutton, stopbutton)
    bot.send_message(message.chat.id, f"Choose your option",
                     reply_markup=markup_menu)
""" Menu after u don't want continue"""

def backMenu(message):
    markup_back = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1,
                                            one_time_keyboard=True)  # задали формат кнопок
    backbutton = types.KeyboardButton("Menu")

    markup_back.add(backbutton)  # добавили кнопки

    bot.send_message(message.chat.id, "hope u find a friend",
                     reply_markup=markup_back)  # подвязали кнопки к сообщению

#def log_user(message):
#    global user



if __name__ == '__main__':
    bot.polling(none_stop=True)

bot.polling(none_stop=True)
