from batya import bot
from telebot import types
#import registration # registration module
import userRegistration
from user import User  # user definition
from database import *

user_dict = {}
DATA_JSON = "data.json"


@bot.message_handler(commands=['start'])  # начинаем
def start(message):
    bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEDUrphmCOr4kukL99zoy9Vop4nguUGqgACQAADOPCiGncMZgcCUVNuIgQ')
    # alex
    #fdsf
    a = 2

    a = 3
    a = 3 * 3
    a = 3 * 3 - 3
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
        #getImage(message)
        user_profile(message) # from registration module
    elif message.text == 'Menu':
        menu(message)


#@bot.message_handler(content_types= ['photo'])
def getImage(message):
    try:
        rawFile = message.photo[2].file_id # photo id
        #print(rawFile)

        photo = rawFile + ".jpg" # photo name
        user_dict['photo'] = photo # save photo name in dictionary

        #print(user_dict['photo'])
        #fileName = user_dict['chatID']
        store = 'DownlodedPhotos/' + rawFile+".jpg" # photo path
        file_info = bot.get_file(rawFile)  # photo description
        #print(file_info)
        downloadFile = bot.download_file(file_info.file_path) # download file like bytes
        with open(store, "wb") as newFile:
            newFile.write(downloadFile)
        print("photo successfully added")
    except Exception as ex:
        print(ex)
    print("Got photo")

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

""" Pегистрация """
def user_profile(message):
    name = bot.send_message(message.chat.id, 'Введи имя')
    chatUserame = message.chat.username
    user_dict['chatUserame'] = chatUserame
    # print(message.chat.first_name) # lesha
    # print(message.chat.last_name) # None
    # print(message.chat.username) # Chat username
    # print(message.chat.id) # chat ID
    bot.register_next_step_handler(name, process_name_step)

def process_name_step(message):
    try:
        chatID = message.chat.id
        name = message.text

        user_dict['chatID'] = chatID
        user_dict['name'] = name

        msg = bot.send_message(message.chat.id, 'Write something about u')
        bot.register_next_step_handler(msg, process_description_step)
    except Exception as e:
        bot.reply_to(message, 'oops')


##############
def process_description_step(message):
    try:
        chatID = message.chat.id
        description = message.text

        user_dict['chatID'] = chatID
        user_dict['desciption'] = description

        msg = bot.send_message(message.chat.id, 'enter image:')
        bot.register_next_step_handler(msg, process_photo_step)
    except Exception as e:
        bot.reply_to(message, 'oops')
###########

###########
def process_photo_step(message):
    try:
        chatID = message.chat.id

        user_dict['chatID'] = chatID

        getImage(message)

        msg = bot.send_message(message.chat.id, 'Where are u from?')
        bot.register_next_step_handler(msg, process_city_step)
    except Exception as e:
        bot.reply_to(message, 'oops')
###########
def process_city_step(message):
    try:
        chatID = message.chat.id
        city = message.text

        user_dict['chatID'] = chatID
        user_dict['city'] = city

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
        user.city = user_dict['city']
        user.describe = user_dict['desciption']
        user.chatUsername = user_dict['chatUserame']
        user.photoName = user_dict['photo']

        if (sex == u'Male') or (sex == u'Female'):
            print(user_dict)
            print(user)
            pass
        else:
            raise Exception("Unknown sex")

        writing(user)
        path = 'DownlodedPhotos/' + user_dict['photo']
        with open(path, 'rb') as file:
            bot.send_photo(message.chat.id, file)

        bot.send_message(user_dict['chatID'],
                        'Nice to meet you, ' + user.name +
                         '\n Age: ' + str(user.age) +
                         '\n Sex: ' + user.sex +
                         '\n City: ' + user.city +
                         '\n Description: ' + user.describe)

    except Exception as e:
        print(e)
        bot.reply_to(message, 'oooops')


if __name__ == '__main__':
    bot.polling(none_stop=True)

bot.polling(none_stop=True)
