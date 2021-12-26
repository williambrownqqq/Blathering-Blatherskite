from batya import bot
from telebot import types
# import registration # registration module
from userRegistration import UserRegistration
from database import *

# user_dict = {}
DATA_JSON = "data.json"


@bot.message_handler(commands=['start'])  # начинаем
def start(message):
    print(message.chat.id)
    bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEDUrphmCOr4kukL99zoy9Vop4nguUGqgACQAADOPCiGncMZgcCUVNuIgQ')
    markup_start_choice = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2,
                                                    one_time_keyboard=True)  # задали формат кнопок
    yes_button = types.KeyboardButton("Yes, i want")
    no_button = types.KeyboardButton("No, i won't")
    markup_start_choice.add(yes_button, no_button)  # добавили кнопки

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
def get_text(message):
    if message.text == 'Yes, i want':  # c кнопки старта переходим в меню
        menu_starter(message)
    elif message.text == "No, i won't":
        bot.send_message(message.chat.id, "exit")  # доделать
        back_menu(message)
    elif message.text == 'Create profile' or message.text == 'Edit my profile':  # create profile
        registration = UserRegistration()
        registration.create_user(message)  # from registration module
    elif message.text == 'Menu':
        menu_starter(message)
    elif message.text == 'Start':
        find_menu(message)
    elif message.text == 'Male' or message.text == 'Female':
        TakeAcc(message)


# @bot.message_handler(content_types= ['photo'])

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
    bot.send_message(message.chat.id, f"Choose your option",
                     reply_markup=markup_menu)


def logged_menu(message):
    markup_menu = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3, one_time_keyboard=True)
    start_button = types.KeyboardButton("Start")
    edit_button = types.KeyboardButton("Edit my profile")
    stop_button = types.KeyboardButton("Stop")
    markup_menu.add(start_button, edit_button, stop_button)
    bot.send_message(message.chat.id, f"Choose your option",
                     reply_markup=markup_menu)


""" Menu after u don't want continue"""


def back_menu(message):
    markup_back = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1,
                                            one_time_keyboard=True)  # задали формат кнопок
    back_button = types.KeyboardButton("Menu")

    markup_back.add(back_button)  # добавили кнопки

    bot.send_message(message.chat.id, "hope u find a friend",
                     reply_markup=markup_back)  # подвязали кнопки к сообщению


def find_menu(message):
    markup_back = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)  # задали формат кнопок
    print("OK")
    back_button = types.KeyboardButton("Menu")
    button1 = types.KeyboardButton("Male")
    button2 = types.KeyboardButton("Female")
    markup_back.add(back_button, button1, button2)
    bot.send_message(message.chat.id, f"Choose your option",
                     reply_markup=markup_back)

# def log_user(message):
#    global user


def TakeAcc(message):
    try:
        if message.text == "Menu":
            menu_starter(message)
        else:
            sqlQuery = f'SELECT * FROM BotUser WHERE UserSex = "{message.text}" and id != {message.chat.id}' \
                       f' order by rand() LIMIT 1;'
            MyCursor.execute(sqlQuery)
            result = MyCursor.fetchone()
            if result:
                print(result[3])
                MyResult = result[4]
                id = result[5]
                store = "ImageOutputs/img{0}.jpg".format(str(id))
                # print(MyResult)

    #            with open(store, "wb") as file:
     #               print(type(MyResult))
      #              file.write(MyResult)  # works with bytes
       #             file.close()
                msg = bot.send_message(message.chat.id, f'[{result[0]}](t.me/{result[7]}), {result[1]}, {result[2]}, '
                                                        f'{result[3]}', parse_mode='Markdown')
            else:
                msg = bot.send_message(message.chat.id, f'No {message.text} in our bot, this is a gay-party')

            print(1)
            bot.register_next_step_handler(msg, TakeAcc)
    except Exception as error:
        print("Failed to grab the photo from table", error)


if __name__ == '__main__':
    bot.polling(none_stop=True)

bot.polling(none_stop=True)
