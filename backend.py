#####################################
#            Created by             #
#                SBR                #
#               zzsxd               #
#####################################
import random
import copy
#####################################


class TempUserData:
    def __init__(self):
        super(TempUserData, self).__init__()
        self.__user_data = {}
        self.__reset = [0, 0, None]

    def temp_data(self, user_id):
        if user_id not in self.__user_data.keys():
            self.__user_data.update({user_id: copy.deepcopy(self.__reset)}) # 3 - status
        return self.__user_data

    def get_all_temp_data(self):
        return self.__user_data

    def reset_user(self, user_id):
        self.temp_data(user_id)[user_id] = copy.deepcopy(self.__reset)


class DbAct:
    def __init__(self, db, config):
        super(DbAct, self).__init__()
        self.__db = db
        self.__config = config

    def get_all_posts(self):
        data = self.__db.db_read('SELECT row_id, photo, content FROM posts', ())
        return data

    def add_post(self, photo, content):
        self.__db.db_write(
            'INSERT INTO posts (photo, content) VALUES (?, ?)',
            (photo, content))

    def del_post(self, post_id):
        self.__db.db_write('DELETE FROM posts WHERE row_id = ?', (post_id, ))

    def get_random_post(self):
        posts_ids_serialised = list()
        posts_ids = self.__db.db_read('SELECT row_id FROM posts', ())
        for i in posts_ids:
            posts_ids_serialised.append(i[0])
        if len(posts_ids_serialised) != 0:
            random_id = random.choice(posts_ids_serialised)
            post = self.__db.db_read('SELECT photo, content FROM posts WHERE row_id = ?', (random_id, ))[0]
            return post

    def add_user(self, user_id, first_name, last_name, nick_name):
        if not self.user_is_existed(user_id):
            if user_id in self.__config.get_config()['admins']:
                is_admin = True
            else:
                is_admin = False
            self.__db.db_write('INSERT INTO users (user_id, first_name, last_name, nick_name, is_admin) VALUES (?, ?, ?, ?, ?)', (user_id, first_name, last_name, nick_name, is_admin))

    def user_is_existed(self, user_id):
        data = self.__db.db_read('SELECT count(*) FROM users WHERE user_id = ?', (user_id, ))
        if len(data) > 0:
            if data[0][0] > 0:
                status = True
            else:
                status = False
            return status

