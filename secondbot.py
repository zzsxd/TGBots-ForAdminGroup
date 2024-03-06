#####################################
#            Created by             #
#                SBR                #
#               zzsxd               #
#####################################
import os
import time
import platform
import telebot
from telebot import types
from threading import Lock
from backend import TempUserData, DbAct
from config_parser import ConfigParser
from db import DB
from frontend import Bot_inline_btns_second

####################################################################
config_name = 'botsecondsecrets.json'


####################################################################
def clear_machine():
    while True:
        for i in temp_user_data.get_all_temp_data().keys():
            temp_user_data.get_all_temp_data()[i][0] = 0
        time.sleep(10)


def is_admin(user_id, admin_ids):
    return user_id in admin_ids


def main():
    @bot.message_handler(commands=['start'])
    def start_msg(message):
        buttons = Bot_inline_btns_second()
        user_name = message.from_user.first_name
        bot.send_message(message.chat.id,
                         f"Привет, {user_name}, я бот для администрирования группы.\nID чата: {message.chat.id}",
                         reply_markup=buttons.start_btns())

    @bot.message_handler(commands=['admin'])
    def admin_msg(message):
        buttons = Bot_inline_btns_second()
        user_id = message.from_user.id
        user_name = message.from_user.first_name
        if is_admin(message.chat.id, admin_ids):
            bot.send_message(message.chat.id, f'Привет!, {user_name}!', reply_markup=buttons.admin_btns())
        else:
            bot.send_message(message.chat.id, 'У вас нет прав на эту команду!')

    @bot.message_handler(content_types=['text'])
    def text(message):
        user_id = message.from_user.id
        temp_user_data.temp_data(user_id)[user_id][0] += 1
        if temp_user_data.temp_data(user_id)[user_id][0] >= 10:
            temp_user_data.temp_data(user_id)[user_id][1] += 1
            if temp_user_data.temp_data(user_id)[user_id][1] == 1:
                bot.reply_to(message, 'Не спамьте!')
            elif temp_user_data.temp_data(user_id)[user_id][1] == 2:
                bot.reply_to(message, 'Не спамьте! Последнее предупреждение!')
            elif temp_user_data.temp_data(user_id)[user_id][1] == 3:
                bot.restrict_chat_member(chat_id=config.get_config()['chat_id'], user_id=user_id)
                bot.send_message(chat_id=config.get_config()['chat_id'], text='Вы были забанены за спам!')
                temp_user_data.reset_user(user_id)


if '__main__' == __name__:
    os_type = platform.system()
    work_dir = os.path.dirname(os.path.realpath(__file__))
    config = ConfigParser(f'{work_dir}/{config_name}', os_type)
    temp_user_data = TempUserData()
    db = DB(config.get_config()['db_file_name'], Lock())
    db_actions = DbAct(db, config)
    bot = telebot.TeleBot(config.get_config()['tg_api'])
    admin_ids = config.get_config()['admins']
    main()
