from main import bot, user_dict
import types
from user import User
from database import writing,convertToBinaryData
# """ Pегистрация """
# def user_profile(message):
#     name = bot.send_message(message.chat.id, 'Введи имя')
#     bot.register_next_step_handler(name, process_name_step)


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
