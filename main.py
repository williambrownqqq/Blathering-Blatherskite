import telebot
import config
import json
from telebot import types
DATA_JSON = "data.json"
bot = telebot.TeleBot(config.TOKEN)
user_dict = {}
class User:
    def __init__(self, name, age):
        self.name = name
        self.age = age
        self.sex = None
    @property
    def age(self):
        return self.__age
    @age.setter
    def age(self, age):
        if not isinstance(age, int):
            raise TypeError("Must be int!")
        if not 14<age<100:
            raise ValueError("Must be higher than 14 and lower than 100")
        self.__age = age

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        if not isinstance(name, str):
            raise TypeError("Must be str")
        self.__name = name

    def __str__(self):
        return f"{self.name} {self.age}"

''' Start '''
@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEDUrphmCOr4kukL99zoy9Vop4nguUGqgACQAADOPCiGncMZgcCUVNuIgQ')
    bot.send_message(message.chat.id,'Привет, хочешь знакомиться?')
    markup = types.ReplyKeyboardMarkup(True, True)
    markup.add(types.KeyboardButton("Да, я хочу знакомств"))
    markup.add(types.KeyboardButton("Нет, я хочу уйти"))
    bot.send_message(message.chat.id, 'Выберите что вам надо', reply_markup=markup)
    #markup.editMessageReplyMarkup(reply_markup=1)
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
