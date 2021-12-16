from batya import bot
from telebot import types
from user import User
from database import writing
""" Логин """
def log_user(message):
    pass
""" Pегистрация """
def create_user(message):
    global user
    name = bot.send_message(message.chat.id, 'Введи имя')
    user = User(message.chat.id)

    user.username = message.chat.username
    bot.register_next_step_handler(name, process_name_step)

def process_name_step(message):
    try:
        user.name = message.text
        msg = bot.send_message(message.chat.id, 'Write something about u')
        bot.register_next_step_handler(msg, process_description_step)
    except Exception as e:
        bot.reply_to(message, 'oops')


##############
def process_description_step(message):
    try:
        user.description = message.text
        msg = bot.send_message(message.chat.id, 'enter image:')
        bot.register_next_step_handler(msg, process_photo_step)
    except Exception as e:
        print(e)
        bot.reply_to(message, 'oops')
###########

###########
def process_photo_step(message):
    try:
        getImage(message, user)
        msg = bot.send_message(message.chat.id, 'Where are u from?')
        bot.register_next_step_handler(msg, process_city_step)
    except Exception as e:
        bot.reply_to(message, 'oops')
###########
def process_city_step(message):
    try:
        try:
            user.city = message.text
        except TypeError:
            msg = bot.send_message(message.chat.id, 'Age should be a string. Where do you live?')
            bot.register_next_step_handler(msg, process_city_step)
            return

        msg = bot.send_message(message.chat.id, 'How old are you?')
        bot.register_next_step_handler(msg, process_age_step)
    except Exception as e:
        bot.reply_to(message, 'oops')

def process_age_step(message):
    try:
        try:
            user.age = int(message.text)
        except TypeError:
            msg = bot.send_message(message.chat.id, 'Age should be a number. How old are you?')
            bot.register_next_step_handler(msg, process_age_step)
            return

        # user = user_dict[chatID]
        # user.age = age

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2, one_time_keyboard=True)
        markup.add('Male', 'Female')
        msg = bot.send_message(message.chat.id, 'What is your gender', reply_markup=markup)
        bot.register_next_step_handler(msg, process_sex_step)
    except Exception as e:
        print(e)
        bot.reply_to(message, 'oooops')

def process_sex_step(message):
    try:
        user.sex = message.text
        process_saveall_step(message)
    except Exception as e:
        print(e)
        bot.reply_to(message, 'oooops')

def process_saveall_step(message):
    try:
        writing(user)
        path = 'DownlodedPhotos/' + user.photo
        with open(path, 'rb') as file:
            bot.send_photo(message.chat.id, file)
        bot.send_message(user.idd,
                     'Nice to meet you, ' + user.name +
                     '\n Age: ' + str(user.age) +
                     '\n Sex: ' + user.sex +
                     '\n City: ' + user.city +
                     '\n Description: ' + user.description)

    except Exception as e:
        print(e)
        bot.reply_to(message, 'oooops')

def getImage(message, user):
    try:
        rawFile = message.photo[2].file_id # photo id
        #print(rawFile)

        photo = rawFile + ".jpg" # photo name
        user.photo = photo # save photo name in dictionary

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