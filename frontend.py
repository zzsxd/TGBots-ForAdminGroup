#####################################
#            Created by             #
#                SBR                #
#               zzsxd               #
#####################################
from telebot import types
#####################################


class Bot_inline_btns_first:
    def __init__(self):
        super(Bot_inline_btns_first, self).__init__()
        self.__markup = types.InlineKeyboardMarkup(row_width=2)

    def start_btns(self):
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        rules = types.KeyboardButton('Правила')
        browser = types.KeyboardButton('Ссылка на браузер')
        on_nego = types.KeyboardButton('Ссылка на него')
        keyboard.add(rules, browser, on_nego)
        return keyboard


    def admin_btns(self):
        create = types.InlineKeyboardButton('Создать пост', callback_data='create_post')
        delete = types.InlineKeyboardButton('Удалить пост', callback_data='delete_post')
        self.__markup.add(create, delete)
        return self.__markup


class Bot_inline_btns_second:
    def __init__(self):
        super(Bot_inline_btns_second, self).__init__()
        self.__markup = types.InlineKeyboardMarkup(row_width=2)

    # def start_btns(self):
    #     gift = types.InlineKeyboardButton('Получить подарок🎁', callback_data='take_gift')
    #     write = types.InlineKeyboardButton('Написать продавцу✍🏼', callback_data='write_manager')
    #     self.__markup.add(gift, write)
    #     return self.__markup

    def start_btns(self):
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        rules = types.KeyboardButton('Правила')
        keyboard.add(rules)
        return keyboard

    def admin_btns(self):
        create = types.InlineKeyboardButton('Создать пост', callback_data='create_post')
        delete = types.InlineKeyboardButton('Удалить пост', callback_data='delete_post')
        self.__markup.add(create, delete)
        return self.__markup


