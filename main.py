#! /usr/bin/env python
# -*- coding: utf-8 -*-
from batya import bot
from telebot import types
# import registration # registration module
from user import User
from database import *
import os

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
        # bot.send_message(message.chat.id, "exit")  # доделать
        # back_menu(message)
        stopMenu = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3, one_time_keyboard=True)
        continueButton = types.KeyboardButton("Continue registration")
        stopMenu.add(continueButton)
        bot.send_message(message.chat.id, f"We will miss u!",
                         reply_markup=stopMenu)
    elif message.text == 'Create profile' or message.text == 'Edit my profile':  # create profile
        registration = UserRegistration()
        registration.create_user(message)  # from registration module
    elif message.text == 'Menu':
        menu_starter(message)
    elif message.text == 'Start' or message.text == 'Continue':
        find_menu(message)
    elif message.text == 'Continue registration':
        menu_starter(message)
    elif message.text == 'Stop':
        stopaction(message)
    elif message.text == 'Male' or message.text == 'Female':
        TakeAcc(message)



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
    bot.send_message(message.chat.id, f"We will miss u!",
                     reply_markup=stopMenu)
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
    try:
        botquery = f"ALTER TABLE botuser ALTER Active SET DEFAULT 1;"
        MyCursor.execute(botquery)
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
                       f' and Active = 1 order by rand() LIMIT 1;'
            MyCursor.execute(sqlQuery)
            result = MyCursor.fetchone()
            if result:
                print(result[3])
                MyResult = result[4]
                id = result[5]
                store = "ImageOutputs/img{0}.jpg".format(str(id))
                # print(MyResult)
                with open(store, "wb") as file:
                    print(type(MyResult))
                    file.write(MyResult)  # works with bytes
                    file.close()
                with open(store, 'rb') as file:
                    msg = bot.send_photo(message.chat.id, file, caption=f'[{result[0]}](t.me/{result[7]}), {result[1]}, '
                                                                  f'{result[2]}, {result[3]}', parse_mode='Markdown')
                try:
                    os.remove(store)
                except OSError:
                    pass
            else:
                msg = bot.send_message(message.chat.id, f'No {message.text} in our bot, this is a gay-party')

            print(1)
            bot.register_next_step_handler(msg, TakeAcc)
    except Exception as error:
        print("Failed to grab the photo from table", error)



class UserRegistration:

    @property
    def user(self):
        return self.__user

    @user.setter
    def user(self, user):
        if not isinstance(user, User):
            raise TypeError("Must be User!")
        self.__user = user

    """ Pегистрация """
    def create_user(self, message):
        try:
            name = bot.send_message(message.chat.id, 'Введи имя')
            self.user = User(message.chat.id)
            self.user.username = message.chat.username
            bot.register_next_step_handler(name, self.process_name_step)
        except Exception as ex:
            print(ex)


    # noinspection PyBroadException
    def process_name_step(self, message):
        try:
            try:
                self.user.name = message.text
            except Exception:
                msg = bot.send_message(message.chat.id, 'Something went wrong. What is your name?')
                bot.register_next_step_handler(msg, self.process_name_step)
                return
            msg = bot.send_message(message.chat.id, 'Write something about u')
            bot.register_next_step_handler(msg, self.process_description_step)
        except Exception as ex:
            print(ex)
            bot.reply_to(message, 'oops')

    ##############
    def process_description_step(self, message):
        try:
            try:
                self.user.description = message.text
            except Exception as ex:
                msg = bot.send_message(message.chat.id, 'Something went wrong. Write something about u')
                bot.register_next_step_handler(msg, self.process_description_step)
                return
            msg = bot.send_message(message.chat.id, 'enter image:')
            bot.register_next_step_handler(msg, self.process_photo_step)
        except Exception as ex:
            print(ex)
            bot.reply_to(message, 'oops')
    ###########

    # noinspection PyBroadException
    def process_photo_step(self, message):
        try:
            try:
                self.user.photoiID = message.photo[2].file_id
                self.get_image(message)
            except Exception as ex:
                msg = bot.send_message(message.chat.id, 'Upload photo again')
                bot.register_next_step_handler(msg, self.process_photo_step)
                return
            msg = bot.send_message(message.chat.id, 'Where are yo from?')
            bot.register_next_step_handler(msg, self.process_city_step)
        except Exception as ex:
            print(f"ex {ex}")
    ###########

    # noinspection PyBroadException
    def process_city_step(self, message):
        try:
            try:
                self.user.city = message.text
            except Exception :
                msg = bot.send_message(message.chat.id, 'Age should be a string. Where do you live?')
                bot.register_next_step_handler(msg, self.process_city_step)
                return

            msg = bot.send_message(message.chat.id, 'How old are you?')
            bot.register_next_step_handler(msg, self.process_age_step)
        except Exception as ex:
            print(ex)
            bot.reply_to(message, 'oops')

    def process_age_step(self, message):
        try:
            try:
                self.user.age = int(message.text)
            except Exception:
                msg = bot.send_message(message.chat.id, 'U should be older than 14. How old are you?')
                bot.register_next_step_handler(msg, self.process_age_step)
                return

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2, one_time_keyboard=True)
            markup.add('Male', 'Female')
            msg = bot.send_message(message.chat.id, 'What is your gender', reply_markup=markup)
            bot.register_next_step_handler(msg, self.process_sex_step)
        except Exception as ex:
            print(ex)
            bot.reply_to(message, 'oooops')

    def process_sex_step(self, message):
        try:
            self.user.sex = message.text
            self.process_saveall_step(message)
        except Exception as ex:
            print(ex)
            bot.reply_to(message, 'oooops')

    def process_saveall_step(self, message):
        try:
            writing(self.user)
            path = 'DownlodedPhotos/' + self.user.photo
            with open(path, 'rb') as file:
                bot.send_photo(message.chat.id, file)
            # bot.send_message(user.idd,
            #              'Nice to meet you, ' + self.user.name +
            #              '\n Age: ' + str(user.age) +
            #              '\n Sex: ' + user.sex +
            #              '\n City: ' + user.city +
            #              '\n Description: ' + user.description)
            bot.send_message(self.user.idd, self.user)
            menu_starter(message)
        except Exception as ex:
            print(ex)
            bot.reply_to(message, 'oooops')

    def get_image(self, message):
        try:
            try:
                # print("yyyy")
                # if message.photo is None:
                #     print("dddd")
                #     Exception("file id empty")

                # print(type(message.photo))
                # raw_file = message.photo[2].file_id  # photo id
                print("message.photo[2].file_id  ", message.photo[2].file_id)

                photo = self.user.photoiID + ".jpg"  # photo name
                self.user.photo = photo  # save photo name in dictionary
            except Exception as ex:
                print(ex)
                msg = bot.send_message(message.chat.id, 'Something went wrong. Upload photo again. ')
                bot.register_next_step_handler(msg, self.process_photo_step)
                return
            # print(rawFile)

            # print(user_dict['photo'])
            # fileName = user_dict['chatID']
            store = 'DownlodedPhotos/' + self.user.photoiID + ".jpg"  # photo path
            file_info = bot.get_file(self.user.photoiID)  # photo description
            # print(file_info)
            download_file = bot.download_file(file_info.file_path)  # download file like bytes
            with open(store, "wb") as newFile:
                newFile.write(download_file)
            print("photo successfully added")
        except Exception as ex:
            print(ex)



if __name__ == '__main__':
    bot.polling(none_stop=True)

bot.polling(none_stop=True)

