from batya import bot
from telebot import types
from user import User
from database import writing
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

        name = bot.send_message(message.chat.id, 'Введи имя')
        self.user = User(message.chat.id)
        self.user.username = message.chat.username
        bot.register_next_step_handler(name, self.process_name_step)

    def process_name_step(self, message):
        try:
            self.user.name = message.text
            msg = bot.send_message(message.chat.id, 'Write something about u')
            bot.register_next_step_handler(msg, self.process_description_step)
        except Exception as e:
            bot.reply_to(message, 'oops')


    ##############
    def process_description_step(self, message):
        try:
            self.user.description = message.text
            msg = bot.send_message(message.chat.id, 'enter image:')
            bot.register_next_step_handler(msg, self.process_photo_step)
        except Exception as e:
            print(e)
            bot.reply_to(message, 'oops')
    ###########

    ###########
    def process_photo_step(self, message):
        try:
            self.getImage(message)
            msg = bot.send_message(message.chat.id, 'Where are u from?')
            bot.register_next_step_handler(msg, self.process_city_step)
        except Exception as e:
            bot.reply_to(message, 'oops')
    ###########
    def process_city_step(self, message):
        try:
            try:
                self.user.city = message.text
            except (TypeError):
                msg = bot.send_message(message.chat.id, 'Age should be a string. Where do you live?')
                bot.register_next_step_handler(msg, self.process_city_step)
                return

            msg = bot.send_message(message.chat.id, 'How old are you?')
            bot.register_next_step_handler(msg, self.process_age_step)
        except Exception as e:
            bot.reply_to(message, 'oops')

    def process_age_step(self, message):
        try:
            try:
                self.user.age = int(message.text)
            except TypeError:
                msg = bot.send_message(message.chat.id, 'Age should be a number. How old are you?')
                bot.register_next_step_handler(msg, self.process_age_step)
                return

            # user = user_dict[chatID]
            # user.age = age

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2, one_time_keyboard=True)
            markup.add('Male', 'Female')
            msg = bot.send_message(message.chat.id, 'What is your gender', reply_markup=markup)
            bot.register_next_step_handler(msg, self.process_sex_step)
        except Exception as e:
            print(e)
            bot.reply_to(message, 'oooops')

    def process_sex_step(self, message):
        try:
            self.user.sex = message.text
            self.process_saveall_step(message)
        except Exception as e:
            print(e)
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
        except Exception as e:
            print(e)
            bot.reply_to(message, 'oooops')

    def getImage(self, message):
        try:
            rawFile = message.photo[2].file_id # photo id
            #print(rawFile)

            photo = rawFile + ".jpg" # photo name
            self.user.photo = photo # save photo name in dictionary

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