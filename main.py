#! /usr/bin/env python
# -*- coding: utf-8 -*-
from batya import bot
from telebot import types
from menu import *


"""
main file, start polling
"""

if __name__ == '__main__':
    bot.polling(none_stop=True)
