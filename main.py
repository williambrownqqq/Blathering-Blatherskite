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
        self.__age = age

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        self.__name = name

    def __str__(self):
        return f'{self.name} {self.age}'
@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id,'Привет, хочешь знакомиться?')
    markup = types.ReplyKeyboardMarkup(True, True)
    markup.add(types.KeyboardButton("Да, я хочу знакомств"))
    markup.add(types.KeyboardButton("Нет, я хочу уйти"))
    bot.send_message(message.chat.id, 'Выберите что вам надо', reply_markup=markup)
@bot.message_handler(content_types='text')
def message_reply(message):
    if message.text=="Да, я хочу знакомств":
        msg = bot.reply_to(message, "Введите свой возраст")
        bot.register_next_step_handler(msg, process_age_step)
    elif message.text=="Нет, я хочу уйти":
        bot.send_message(message.chat.id,'Спасибо за прочтение статьи!')

def process_age_step(message):
    try:
        chat_id = message.chat.id
        age = message.text
        user = User(message.from_user.username, age)
        user_dict[chat_id] = user
        print(User)
        msg = bot.reply_to(message, 'Ты тупой?')
        bot.register_next_step_handler(msg, process_dumb_step)
    except Exception as e:
        bot.reply_to(message, 'oooops')
def process_dumb_step(message):
    pass
@bot.message_handler(commands=['auth'])
def send_auth(message):
    pass
bot.polling(none_stop=True, interval=0)
# def get_text_messages(message):
#     # Если написали «Привет»
#     if message.text == "Привет":
#         # Пишем приветствие
#         bot.send_message(message.from_user.id, "Привет, сейчас я расскажу тебе гороскоп на сегодня.")
#         # Готовим кнопки
#         keyboard = types.InlineKeyboardMarkup()
#         # По очереди готовим текст и обработчик для каждого знака зодиака
#         key_oven = types.InlineKeyboardButton(text='Овен', callback_data='zodiac')
#         # И добавляем кнопку на экран
#         keyboard.add(key_oven)
#         key_telec = types.InlineKeyboardButton(text='Телец', callback_data='zodiac')
#         keyboard.add(key_telec)
#         key_bliznecy = types.InlineKeyboardButton(text='Близнецы', callback_data='zodiac')
#         keyboard.add(key_bliznecy)
#         key_rak = types.InlineKeyboardButton(text='Рак', callback_data='zodiac')
#         keyboard.add(key_rak)
#         key_lev = types.InlineKeyboardButton(text='Лев', callback_data='zodiac')
#         keyboard.add(key_lev)
#         key_deva = types.InlineKeyboardButton(text='Дева', callback_data='zodiac')
#         keyboard.add(key_deva)
#         key_vesy = types.InlineKeyboardButton(text='Весы', callback_data='zodiac')
#         keyboard.add(key_vesy)
#         key_scorpion = types.InlineKeyboardButton(text='Скорпион', callback_data='zodiac')
#         keyboard.add(key_scorpion)
#         key_strelec = types.InlineKeyboardButton(text='Стрелец', callback_data='zodiac')
#         keyboard.add(key_strelec)
#         key_kozerog = types.InlineKeyboardButton(text='Козерог', callback_data='zodiac')
#         keyboard.add(key_kozerog)
#         key_vodoley = types.InlineKeyboardButton(text='Водолей', callback_data='zodiac')
#         keyboard.add(key_vodoley)
#         key_ryby = types.InlineKeyboardButton(text='Рыбы', callback_data='zodiac')
#         keyboard.add(key_ryby)
#         # Показываем все кнопки сразу и пишем сообщение о выборе
#         bot.send_message(message.from_user.id, text='Выбери свой знак зодиака', reply_markup=keyboard)
#     elif message.text == "/help":
#         bot.send_message(message.from_user.id, "Напиши Привет")
#     else:
#         bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help.")
# # Обработчик нажатий на кнопки
# @bot.callback_query_handler(func=lambda call: True)
# def callback_worker(call):
#     # Если нажали на одну из 12 кнопок — выводим гороскоп
#     if call.data == "zodiac":
#         # Формируем гороскоп
#         msg = random.choice(first) + ' ' + random.choice(second) + ' ' + random.choice(second_add) + ' ' + random.choice(third)
#         # Отправляем текст в Телеграм
#         bot.send_message(call.message.chat.id, msg)
# # Запускаем постоянный опрос бота в Телеграме
