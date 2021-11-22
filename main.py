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


""" start command processing """
"""@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEDUrphmCOr4kukL99zoy9Vop4nguUGqgACQAADOPCiGncMZgcCUVNuIgQ')
    bot.send_message(message.chat.id,'Привет, хочешь знакомиться?')
    markup = types.ReplyKeyboardMarkup(True, True)
    markup.add(types.KeyboardButton("Да, я хочу знакомств"))
    markup.add(types.KeyboardButton("Нет, я хочу уйти"))
    bot.send_message(message.chat.id, 'Выберите что вам надо', reply_markup=markup)
    #markup.editMessageReplyMarkup(reply_markup=1)"""


""" text command processing """
"""
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
"""


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEDUrphmCOr4kukL99zoy9Vop4nguUGqgACQAADOPCiGncMZgcCUVNuIgQ')
    bot.send_message(message.chat.id, 'Привет, хочешь знакомиться?')
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(types.KeyboardButton("Да, я хочу знакомств"))
    markup.add(types.KeyboardButton("Нет, я хочу уйти"))
    msg = bot.send_message(message.chat.id, 'Выберите что вам надо', reply_markup=markup)
    bot.register_next_step_handler(msg, menu)
    # markup.editMessageReplyMarkup(reply_markup=1)


@bot.message_handler(content_types=['text'])
def menu(message):
    types.ReplyKeyboardRemove()
    bot.send_message(message.chat.id, 'Hello')
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True, row_width=2)
    btn0 = types.KeyboardButton("Мой профиль")
    btn1 = types.KeyboardButton("Настройки поиска")
    btn2 = types.KeyboardButton("Ищем любовь")
    btn3 = types.KeyboardButton("Кому я нравлюсь")
    btn4 = types.KeyboardButton("Копейка в развитие")
    markup.add(btn0, btn1, btn2, btn3, btn4)
    bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEDUrphmCOr4kukL99zoy9Vop4nguUGqgACQAADOPCiGncMZgcCUVNuIgQ')
    start_handler = f"<b>Что дальше, {message.from_user.first_name}?</b>"
    msg = bot.send_message(message.chat.id, start_handler, parse_mode='html', reply_markup=markup)
    bot.register_next_step_handler(msg, menu_next)


def menu_next(message):
    get_message_bot = message.text
    if get_message_bot == "Мой профиль":
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True, row_width=2)
        btn0 = types.KeyboardButton("Заполнить профиль")
        btn1 = types.KeyboardButton("Удалить профиль")
        btn2 = types.KeyboardButton("Главное меню")
        markup.add(btn0, btn1)
        markup.add(btn2)
        msg = bot.send_message(message.chat.id, "Profile", parse_mode='html', reply_markup=markup)
        bot.register_next_step_handler(msg, profile_next)

    elif get_message_bot == "Настройки поиска":
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True, row_width=1)
        btn0 = types.KeyboardButton("Заполнить поиск")
        btn1 = types.KeyboardButton("Главное меню")
        markup.add(btn0, btn1)
        msg = bot.send_message(message.chat.id, "find_settings", parse_mode='html', reply_markup=markup)
        bot.register_next_step_handler(msg, find_settings_next)
    elif get_message_bot == "Ищем любовь":
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True, row_width=1)
        btn1 = types.KeyboardButton("Главное меню")
        markup.add(btn1)
        msg = bot.send_message(message.chat.id, "find_love", parse_mode='html', reply_markup=markup)
        bot.register_next_step_handler(msg, find_love_next)
    elif get_message_bot == "Кому я нравлюсь":
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True, row_width=1)
        btn1 = types.KeyboardButton("Главное меню")
        markup.add(btn1)
        msg = bot.send_message(message.chat.id, "finded_love", parse_mode='html', reply_markup=markup)
        bot.register_next_step_handler(msg, finded_love_next)
    elif get_message_bot == "Копейка в развитие":
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True, row_width=1)
        btn1 = types.KeyboardButton("Главное меню")
        markup.add(btn1)
        msg = bot.send_message(message.chat.id, "sponsor", parse_mode='html', reply_markup=markup)
        bot.register_next_step_handler(msg, sponsor_next)
    else:
        bot.send_message(message.chat.id, "6", parse_mode='html')
        bot.register_next_step_handler(message, menu)


def sponsor_next(message):
    get_message_bot = message.text
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True, row_width=2)
    btn0 = types.KeyboardButton("Мой профиль")
    btn1 = types.KeyboardButton("Настройки поиска")
    btn2 = types.KeyboardButton("Ищем любовь")
    btn3 = types.KeyboardButton("Кому я нравлюсь")
    btn4 = types.KeyboardButton("Копейка в развитие")
    markup.add(btn0, btn1, btn2, btn3, btn4)
    bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEDUrphmCOr4kukL99zoy9Vop4nguUGqgACQAADOPCiGncMZgcCUVNuIgQ')
    start_handler = f"<b>Что дальше, {message.from_user.first_name}?</b>"
    msg = bot.send_message(message.chat.id, start_handler, parse_mode='html', reply_markup=markup)

    if get_message_bot == "Главное меню":
        bot.register_next_step_handler(msg, menu_next)
    else:
        bot.send_message(message.chat.id, "Неправильный ввод", parse_mode='html')
        bot.register_next_step_handler(message, find_settings_next)


def finded_love_next(message):
    get_message_bot = message.text
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True, row_width=2)
    btn0 = types.KeyboardButton("Мой профиль")
    btn1 = types.KeyboardButton("Настройки поиска")
    btn2 = types.KeyboardButton("Ищем любовь")
    btn3 = types.KeyboardButton("Кому я нравлюсь")
    btn4 = types.KeyboardButton("Копейка в развитие")
    markup.add(btn0, btn1, btn2, btn3, btn4)
    bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEDUrphmCOr4kukL99zoy9Vop4nguUGqgACQAADOPCiGncMZgcCUVNuIgQ')
    start_handler = f"<b>Что дальше, {message.from_user.first_name}?</b>"
    msg = bot.send_message(message.chat.id, start_handler, parse_mode='html', reply_markup=markup)

    if get_message_bot == "Главное меню":
        bot.register_next_step_handler(msg, menu_next)
    else:
        bot.send_message(message.chat.id, "Неправильный ввод", parse_mode='html')
        bot.register_next_step_handler(message, find_settings_next)


def find_love_next(message):
    get_message_bot = message.text
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True, row_width=2)
    btn0 = types.KeyboardButton("Мой профиль")
    btn1 = types.KeyboardButton("Настройки поиска")
    btn2 = types.KeyboardButton("Ищем любовь")
    btn3 = types.KeyboardButton("Кому я нравлюсь")
    btn4 = types.KeyboardButton("Копейка в развитие")
    markup.add(btn0, btn1, btn2, btn3, btn4)
    bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEDUrphmCOr4kukL99zoy9Vop4nguUGqgACQAADOPCiGncMZgcCUVNuIgQ')
    start_handler = f"<b>Что дальше, {message.from_user.first_name}?</b>"
    msg = bot.send_message(message.chat.id, start_handler, parse_mode='html', reply_markup=markup)

    if get_message_bot == "Главное меню":
        bot.register_next_step_handler(msg, menu_next)
    else:
        bot.send_message(message.chat.id, "Неправильный ввод", parse_mode='html')
        bot.register_next_step_handler(message, find_settings_next)


def find_settings_next(message):
    get_message_bot = message.text
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True, row_width=2)
    btn0 = types.KeyboardButton("Мой профиль")
    btn1 = types.KeyboardButton("Настройки поиска")
    btn2 = types.KeyboardButton("Ищем любовь")
    btn3 = types.KeyboardButton("Кому я нравлюсь")
    btn4 = types.KeyboardButton("Копейка в развитие")
    markup.add(btn0, btn1, btn2, btn3, btn4)
    bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEDUrphmCOr4kukL99zoy9Vop4nguUGqgACQAADOPCiGncMZgcCUVNuIgQ')
    start_handler = f"<b>Что дальше, {message.from_user.first_name}?</b>"
    msg = bot.send_message(message.chat.id, start_handler, parse_mode='html', reply_markup=markup)

    if get_message_bot == "Заполнить поиск":
        bot.send_message(message.chat.id, "Ребят тут делаем заполнение предпочтений", parse_mode='html')
        bot.register_next_step_handler(msg, menu_next)
    elif get_message_bot == "Главное меню":
        bot.register_next_step_handler(msg, menu_next)
    else:
        bot.send_message(message.chat.id, "Неправильный ввод", parse_mode='html')
        bot.register_next_step_handler(message, find_settings_next)


def profile_next(message):
    get_message_bot = message.text
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True, row_width=2)
    btn0 = types.KeyboardButton("Мой профиль")
    btn1 = types.KeyboardButton("Настройки поиска")
    btn2 = types.KeyboardButton("Ищем любовь")
    btn3 = types.KeyboardButton("Кому я нравлюсь")
    btn4 = types.KeyboardButton("Копейка в развитие")
    markup.add(btn0, btn1, btn2, btn3, btn4)
    bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEDUrphmCOr4kukL99zoy9Vop4nguUGqgACQAADOPCiGncMZgcCUVNuIgQ')
    start_handler = f"<b>Что дальше, {message.from_user.first_name}?</b>"
    msg = bot.send_message(message.chat.id, start_handler, parse_mode='html', reply_markup=markup)

    if get_message_bot == "Заполнить профиль":
        bot.send_message(message.chat.id, "Ребят тут делаем заполнение аккаунта", parse_mode='html')
        bot.register_next_step_handler(msg, menu_next)
    elif get_message_bot == "Удалить профиль":
        bot.send_message(message.chat.id, "Удалил профиль", parse_mode='html')
        bot.register_next_step_handler(msg, menu_next)
    elif get_message_bot == "Главное меню":
        bot.send_message(message.chat.id, "Главное меню", parse_mode='html')
        bot.register_next_step_handler(msg, menu_next)
    else:
        bot.send_message(message.chat.id, "Неправильный ввод", parse_mode='html')
        bot.register_next_step_handler(message, profile_next)






if __name__ == '__main__':
    bot.polling(none_stop=True)

bot.polling(none_stop=True)
