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
from backend import TempUserData
from config_parser import ConfigParser
from frontend import Bot_inline_btns_first

####################################################################
config_name = 'botfirstsecrets.json'
last_message_times = {}  # Список для отслеживания пользователей и времени их последнего сообщения
posts = {}  # Словарь для хранения созданных постов
####################################################################


def clear_machine():
    while True:
        print(temp_user_data.get_all_temp_data())
        for i in temp_user_data.get_all_temp_data().keys():
            temp_user_data.get_all_temp_data()[i][0] = 0
            print(temp_user_data.get_all_temp_data()[i][0])
        time.sleep(5)


def main():
    @bot.message_handler(commands=['start'])
    def start_msg(message):
        buttons = Bot_inline_btns_first()
        user_name = message.from_user.first_name
        bot.send_message(message.chat.id, f"Привет, {user_name}, я бот для администрирования группы.\nID чата: {message.chat.id}",
                         reply_markup=buttons.start_btns())

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
                temp_user_data.reset_user(user_id)

    @bot.message_handler(func=lambda message: True)
    def handle_message(message):
        user_id = message.from_user.id
        current_time = time.time()

        # Проверка на спам: если пользователь отправляет сообщения слишком быстро, считаем его сообщения спамом
        if user_id in last_message_times and current_time - last_message_times[user_id] < 5:
            bot.reply_to(message, "Пожалуйста, перестаньте отправлять сообщения так быстро.")
        else:
            # Если сообщение не является спамом, обработка сообщения по умолчанию
            # (короче тут это  - эхо-ответ на сообщение пользователя)
            last_message_times[user_id] = current_time  # Обновляем время последнего сообщения пользователя
            bot.reply_to(message, message.text)

    # команда /newpost для создания нового поста
    @bot.message_handler(commands=['newpost'])
    def handle_newpost(message):
        bot.reply_to(message, "Введите текст нового поста:")
        bot.register_next_step_handler(message, create_new_post)

    # Создание нового поста
    def create_new_post(message):
        user_id = message.from_user.id
        posts[user_id] = message.text
        bot.reply_to(message, "Пост создан. Чтобы выполнить рассылку, введите /sendpost")

    # команда /sendpost для рассылки созданного поста в группу
    @bot.message_handler(commands=['sendpost'])
    def handle_sendpost(message):
        user_id = message.from_user.id
        if user_id in posts:
            post_text = posts[user_id]
            bot.send_message(chat_id, post_text)
            bot.reply_to(message, "Пост успешно отправлен в группу.")
        else:
            bot.reply_to(message, "Сначала создайте новый пост с помощью команды /newpost")

    bot.polling(none_stop=True)


if '__main__' == __name__:
    os_type = platform.system()
    work_dir = os.path.dirname(os.path.realpath(__file__))
    config = ConfigParser(f'{work_dir}/{config_name}', os_type)
    temp_user_data = TempUserData()
    time_machine = threading.Thread(target=clear_machine).start()
    bot = telebot.TeleBot(config.get_config()['tg_api'])
    main()
