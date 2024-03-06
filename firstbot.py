#####################################
#            Created by             #
#                SBR                #
#               zzsxd               #
#####################################
import os
import time
import platform
import telebot
import threading
from threading import Lock
from backend import TempUserData, DbAct
from config_parser import ConfigParser
from frontend import Bot_inline_btns_first
from db import DB
####################################################################
config_name = 'botfirstsecrets.json'
last_message_times = {}  # Список для отслеживания пользователей и времени их последнего сообщения
posts = {}  # Словарь для хранения созданных постов
####################################################################


def clear_machine():
    while True:
        for i in temp_user_data.get_all_temp_data().keys():
            temp_user_data.get_all_temp_data()[i][0] = 0
        time.sleep(10)

def create_new_post(message):
    user_id = message.from_user.id
    posts[user_id] = message.text
    bot.reply_to(message, "Пост создан. Чтобы выполнить рассылку, введите /sendpost")

def is_admin(user_id, admin_ids):
    return user_id in admin_ids


def main():
    @bot.message_handler(commands=['start', 'admin', 'sendpost'])
    def start_msg(message):
        user_id = message.from_user.id
        user_name = message.from_user.first_name
        command = message.text.replace('/', '')
        buttons = Bot_inline_btns_first()
        if command == 'start':
            user_name = message.from_user.first_name
            bot.send_message(message.chat.id, f"Привет, {user_name}, я бот для администрирования группы.\nID чата: {message.chat.id}",
                             reply_markup=buttons.start_btns())
        elif is_admin(user_id, admin_ids):
            if command == 'admin':
                bot.send_message(message.chat.id, f'Привет!, {user_name}!', reply_markup=buttons.admin_btns())
            elif command == 'sendpost':
                data = db_actions.get_random_post()
                if data is not None:
                    bot.send_photo(chat_id=config.get_config()['chat_id'], caption=data[1], photo=data[0])
                else:
                    bot.send_message(user_id, text='Сначала создайте пост /admin')

    @bot.message_handler(content_types=['text', 'photo'])
    def text(message):
        print(temp_user_data.get_all_temp_data())
        user_input = message.text
        photo = message.photo
        user_id = message.from_user.id
        print(user_id)
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
        if temp_user_data.temp_data(user_id)[user_id][2] == 1:
            if user_input is not None:
                db_actions.del_post(user_input)
                temp_user_data.temp_data(user_id)[user_id][2] = None
                bot.send_message(message.chat.id, 'Пост удалён')
            else:
                bot.send_message(message.chat.id, 'Это не текст')
        elif temp_user_data.temp_data(user_id)[user_id][2] == 2:
            if photo is not None:
                photo_forward_id = message.id
                temp_user_data.temp_data(user_id)[user_id][3][1] = photo_forward_id
                photo_id = photo[-1].file_id
                photo_file = bot.get_file(photo_id)
                photo_bytes = bot.download_file(photo_file.file_path)
                temp_user_data.temp_data(user_id)[user_id][3][1] = photo_bytes
                temp_user_data.temp_data(user_id)[user_id][2] = 3
                bot.send_message(message.chat.id, 'Введите контент поста')
            else:
                bot.send_message(message.chat.id, 'Это не фото')
        elif temp_user_data.temp_data(user_id)[user_id][2] == 3:
            if user_input is not None:
                temp_user_data.temp_data(user_id)[user_id][3][2] = user_input
                temp_user_data.temp_data(user_id)[user_id][2] = None
                db_actions.add_post(temp_user_data.temp_data(user_id)[user_id][3][1], temp_user_data.temp_data(user_id)[user_id][3][2])
                bot.send_message(message.chat.id, 'Пост добавлен')
            else:
                bot.send_message(message.chat.id, 'Это не текст')

    @bot.callback_query_handler(func=lambda call: True)
    def callback(call):
        user_id = call.message.chat.id
        if call.data == 'create_post':
            bot.send_message(call.message.chat.id, 'Отправьте фото поста')
            temp_user_data.temp_data(user_id)[user_id][2] = 2
        elif call.data == 'delete_post':
            for i in db_actions.get_all_posts():
                bot.send_photo(chat_id=call.message.chat.id, caption=f'ID поста: {i[0]}\nОписание: {i[2]}', photo=i[1])
            bot.send_message(call.message.chat.id, 'Введите ID поста: ')
            temp_user_data.temp_data(user_id)[user_id][2] = 1

    bot.polling(none_stop=True)


if '__main__' == __name__:
    os_type = platform.system()
    work_dir = os.path.dirname(os.path.realpath(__file__))
    config = ConfigParser(f'{work_dir}/{config_name}', os_type)
    temp_user_data = TempUserData()
    db = DB(config.get_config()['db_file_name'], Lock())
    db_actions = DbAct(db, config)
    time_machine = threading.Thread(target=clear_machine).start()
    bot = telebot.TeleBot(config.get_config()['tg_api'])
    admin_ids = config.get_config()['admins']
    main()
