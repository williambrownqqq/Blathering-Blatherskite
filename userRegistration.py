import menu
from batya import bot
from telebot import types
from user import User
from database import save_all
import os


class UserRegistration:
    """
    Class for user registration, wonderful
    """
    """
    attributes:
    user: user, pretty handsome and also very wonderful     
    """
    @property
    def user(self):
        return self.__user

    @user.setter
    def user(self, user):
        if not isinstance(user, User):
            raise TypeError("Must be User!")
        self.__user = user

    """ registration """
    def create_user(self, message):
        """
        function to initialisation class User in class UserRegistration
        """
        try:
            name = bot.send_message(message.chat.id, 'enter a name', reply_markup = types.ReplyKeyboardRemove())
            self.user = User(message.chat.id)
            self.user.username = message.chat.username
            bot.register_next_step_handler(name, self.process_name_step)
        except Exception as ex:
            print(ex)

    def process_name_step(self, message):
        """
        step of entering name during registration
        """
        try:
            try:
                self.user.name = message.text
            except TypeError:
                msg = bot.send_message(message.chat.id, 'Something went wrong. What is your name?')
                bot.register_next_step_handler(msg, self.process_name_step)
                return
            except ValueError:
                msg = bot.send_message(message.chat.id, 'Your name is too short or contains not only letters. What is your name?')
                bot.register_next_step_handler(msg, self.process_name_step)
                return
            msg = bot.send_message(message.chat.id, 'Write something about u')
            bot.register_next_step_handler(msg, self.process_description_step)
        except Exception as ex:
            print(ex)
            bot.reply_to(message, 'oops')

    def process_description_step(self, message):
        """
        step of entering acc description during registration
        """
        try:
            try:
                self.user.description = message.text
            except TypeError:
                msg = bot.send_message(message.chat.id, 'Something went wrong. Write something about u')
                bot.register_next_step_handler(msg, self.process_description_step)
                return
            msg = bot.send_message(message.chat.id, 'enter image:')
            bot.register_next_step_handler(msg, self.process_photo_step)
        except Exception as ex:
            print(ex)
            bot.reply_to(message, 'oops')

    def process_photo_step(self, message):
        """
        step of entering photo during registration
        """
        try:
            try:
                self.user.photo_id = message.photo[2].file_id
                self.get_image(message)
            except TypeError:
                msg = bot.send_message(message.chat.id, 'Upload photo again')
                bot.register_next_step_handler(msg, self.process_photo_step)
                return
            msg = bot.send_message(message.chat.id, 'Where are you studying?')
            bot.register_next_step_handler(msg, self.process_university_step)
        except Exception as ex:
            print(f"ex {ex}")

    def process_university_step(self, message):
        """
        step of entering study place during registration
        """
        try:
            try:
                self.user.university = message.text
            except TypeError:
                msg = bot.send_message(message.chat.id, 'University should be a string. Where are you studying?')
                bot.register_next_step_handler(msg, self.process_university_step)
                return
            except ValueError:
                msg = bot.send_message(message.chat.id, 'University should contain only letters. Where are you studying?')
                bot.register_next_step_handler(msg, self.process_university_step)
                return

            msg = bot.send_message(message.chat.id, 'How old are you?')
            bot.register_next_step_handler(msg, self.process_age_step)
        except Exception as ex:
            print(ex)
            bot.reply_to(message, 'oops')

    def process_age_step(self, message):
        """
        step of entering age during registration
        """
        try:
            try:
                self.user.age = int(message.text)
            except TypeError:
                msg = bot.send_message(message.chat.id, 'Please, enter a number. How old are you?')
                bot.register_next_step_handler(msg, self.process_age_step)
                return
            except ValueError:
                msg = bot.send_message(message.chat.id, 'Age should be between 14 and 100. How old are you?')
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
        """
        step of sex during registration
        """
        try:
            try:
                self.user.sex = message.text
                self.process_save_all_step(message)
            except TypeError:
                msg = bot.send_message(message.chat.id, 'Something went wrong. Try again.')
                bot.register_next_step_handler(msg, self.process_sex_step)
                return
        except Exception as ex:
            print(ex)
            bot.reply_to(message, 'oooops')

    def process_save_all_step(self, message):
        """
        save new or edit acc in db and show acc to user
        """
        try:
            save_all(self.user)
            path = 'DownloadedPhotos/' + self.user.photo
            with open(path, 'rb') as file:
                bot.send_photo(message.chat.id, file)
            bot.send_message(self.user.idd, self.user)
            bot.send_message(self.user.idd, "Now you are visible for others.")
            menu.menu_starter(message)
            try:
                os.remove(path)
            except OSError:
                pass
        except Exception as ex:
            print(ex)
            bot.reply_to(message, 'Wrong')

    def get_image(self, message):
        """
        function to get and save photo from user message
        """
        try:
            try:
                print("message.photo[2].file_id  ", message.photo[2].file_id)
                photo = self.user.photo_id + ".jpg"  # photo name
                self.user.photo = photo
            except TypeError:
                msg = bot.send_message(message.chat.id, 'Something went wrong. Upload photo again. ')
                bot.register_next_step_handler(msg, self.process_photo_step)
                return

            store = 'DownloadedPhotos/' + self.user.photo_id + ".jpg"  # photo path
            file_info = bot.get_file(self.user.photo_id)  # photo description
            download_file = bot.download_file(file_info.file_path)  # download file like bytes
            with open(store, "wb") as newFile:
                newFile.write(download_file)
            print("photo successfully added")
        except Exception as ex:
            print(ex)
            