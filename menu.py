from batya import bot
from telebot import types
from userRegistration import UserRegistration
from database import *
import os

@bot.message_handler(commands=['start'])  # начинаем
def start(message):
    print(message.chat.id)
    bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEDUrphmCOr4kukL99zoy9Vop4nguUGqgACQAADOPCiGncMZgcCUVNuIgQ')
    markup_start_choice = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2,
                                                    one_time_keyboard=True)  # задали формат кнопок
    yes_button = types.KeyboardButton("Yes, i want")
    no_button = types.KeyboardButton("No, i won't")
    markup_start_choice.add(yes_button, no_button)  # добавили кнопки

    bot.send_message(message.chat.id, "Hi, let's start?",
                     reply_markup=markup_start_choice)  # подвязали кнопки к сообщению


@bot.message_handler(content_types=['text'])  # обрабатываем кнопки клавиатуры
def get_text(message):
    if message.text == 'Yes, i want':  # c кнопки старта переходим в меню
        menu_starter(message)
    elif message.text == "No, i won't":
        stopMenu = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3, one_time_keyboard=True)
        continueButton = types.KeyboardButton("Continue registration")
        stopMenu.add(continueButton)
        bot.send_message(message.chat.id, 'We will miss you!', reply_markup=stopMenu)
    elif message.text == 'Continue registration':
        menu_starter(message)
    elif message.text == 'Stop':
        stopaction(message)
    else:
        bot.send_message(message.chat.id, "Something went wrong")
        back_menu(message)

@bot.message_handler(commands=['stop'])
def stopaction(message):
    try:
        id = message.chat.id
        active = 0
        botquery = f"UPDATE botuser SET Active = %s WHERE ID = %s "
        data = (active, id)
        MyCursor.execute(botquery, data)
        Myconnector.commit()
        print("Successfully connect!")
    except Exception as ex:
        print("Connection refused!")
        print(ex)

    stopMenu = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3, one_time_keyboard=True)
    continueButton = types.KeyboardButton("Continue")
    stopMenu.add(continueButton)
    msg = bot.send_message(message.chat.id, f"Now you are invisible for others. We will miss u!",
                     reply_markup=stopMenu)
    bot.register_next_step_handler(msg, find_menu)

""" regular menu """


def menu_starter(message):
    if checkuser(message.chat.username):
        logged_menu(message)
    else:
        guest_menu(message)

def guest_menu(message):
    markup_menu = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3, one_time_keyboard=True)
    profile_button = types.KeyboardButton("Create profile")
    stop_button = types.KeyboardButton("Stop")
    markup_menu.add(profile_button, stop_button)
    msg = bot.send_message(message.chat.id, f"Choose your option",
                     reply_markup=markup_menu)
    bot.register_next_step_handler(msg, guest_menu_text)

def logged_menu(message):
    markup_menu = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3, one_time_keyboard=True)
    start_button = types.KeyboardButton("Find someone")
    edit_button = types.KeyboardButton("Edit my profile")
    stop_button = types.KeyboardButton("Stop")
    markup_menu.add(start_button, edit_button, stop_button)
    msg = bot.send_message(message.chat.id, f"Choose your option",
                           reply_markup=markup_menu)
    bot.register_next_step_handler(msg, logged_menu_text)

def guest_menu_text(message):
    if message.text == 'Create profile':  # create profile
        registration = UserRegistration()
        registration.create_user(message)  # from registration module
    elif message.text == 'Stop':
        stopaction(message)
    else:
        bot.send_message(message.chat.id, "Incorrect input")
        bot.register_next_step_handler(message, guest_menu_text)

def logged_menu_text(message):
    print("guest menu")
    if message.text == "Find someone":
        find_menu(message)
    elif message.text == 'Edit my profile':  # create profile
        registration = UserRegistration()
        registration.create_user(message)  # from registration module
    elif message.text == 'Stop':
        stopaction(message)
    else:
        bot.send_message(message.chat.id, "Incorrect input")
        bot.register_next_step_handler(message, guest_menu_text)

""" Menu after u don't want continue"""
def back_menu(message):
    markup_back = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1,
                                            one_time_keyboard=True)  # задали формат кнопок
    back_button = types.KeyboardButton("Menu")

    markup_back.add(back_button)  # добавили кнопки

    msg = bot.send_message(message.chat.id, "hope u find a friend",
                     reply_markup=markup_back)  # подвязали кнопки к сообщению
    bot.register_next_step_handler(msg, menu_starter)

def find_menu(message):
    try:
        id = message.chat.id
        active = 1
        botquery = f"UPDATE botuser SET Active = %s WHERE ID = %s "
        data = (active, id)
        MyCursor.execute(botquery, data)

        Myconnector.commit()
        print("Successfully connect!")
    except Exception as ex:
        print("Connection refused!")
        print(ex)

    markup_back = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)  # задали формат кнопок
    print("Finding is OK")
    back_button = types.KeyboardButton("Menu")
    button1 = types.KeyboardButton("Find male")
    button2 = types.KeyboardButton("Find female")
    markup_back.add(back_button, button1, button2)
    msg = bot.send_message(message.chat.id, f"Choose your option",
                     reply_markup=markup_back)
    bot.register_next_step_handler(msg, TakeAcc)

def TakeAcc(message):
    try:
        if message.text == "Menu":
            menu_starter(message)
        else:
            if message.text == "Find male":
                text = "Male"
            elif message.text == "Find female":
                text = "Female"
            else:
                bot.send_message(message.chat.id, 'Press buttons')
            sqlQuery = f'SELECT * FROM botuser WHERE UserSex = "{text}" and id != {message.chat.id}' \
                       f' and Active = 1 order by rand() LIMIT 3;'
            MyCursor.execute(sqlQuery)
            result = MyCursor.fetchall()
            if result:
                for person in result:
                    print(person[3])
                    MyResult = person[4]
                    id = person[5]
                    store = "ImageOutputs/img{0}.jpg".format(str(id))
                    with open(store, "wb") as file:
                        file.write(MyResult)  # works with bytes
                        file.close()
                    with open(store, 'rb') as file:
                        msg = bot.send_photo(message.chat.id, file, caption=f'[{person[0]}](t.me/{person[7]}), {person[1]}, '
                                                                      f'{person[2]}, {person[3]}', parse_mode='Markdown')
                    try:
                        os.remove(store)
                    except OSError:
                        pass
            else:
                msg = bot.send_message(message.chat.id, f'No {text} in our bot, this is a gay-party')
            bot.register_next_step_handler(msg, TakeAcc)
    except Exception as error:
        print("Failed to grab the photo from table", error)
