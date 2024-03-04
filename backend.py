#####################################
#            Created by             #
#                SBR                #
#               zzsxd               #
#####################################
import time
from datetime import datetime

#####################################


class TempUserData:
    def __init__(self):
        super(TempUserData, self).__init__()
        self.__user_data = {}

    def temp_data(self, user_id):
        if user_id not in self.__user_data.keys():
            self.__user_data.update({user_id: [None, [None, None, None, None, None, None], None, None, None]}) # 1 - status, 2 - m
        return self.__user_data



class DbAct:
    def __init__(self, db, config):
        super(DbAct, self).__init__()
        self.__db = db
        self.__config = config

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

    def user_is_admin(self, user_id):
        data = self.__db.db_read('SELECT is_admin FROM users WHERE user_id = ?', (user_id, ))
        if len(data) > 0:
            if data[0][0] == 1:
                status = True
            else:
                status = False
            return status

    def get_sale_by_id(self, sale_id):
        s = ''
        data = self.__db.db_read(f'SELECT time, key, price FROM sales WHERE product = ?', (sale_id, ))
        for i in data:
            s += f"Время покупки: {datetime.utcfromtimestamp(i[0]).strftime('%Y-%m-%d %H:%M')}\nКлюч: {i[1]}\nСумма покупки: {i[2]} ₽\n\n"
        return s

    def add_one_product(self, data):
        data = self.__db.db_read('SELECT MAX(row_id) FROM products', ())
        if len(data) > 0:
            new_id = int(data[0][0]) + 1
        else:
            new_id = 1
        self.__db.db_write(f'INSERT INTO products (row_id, photo, price, key, description, category, preview) VALUES ({new_id}, ?, ?, ?, ?, ?, ?)', data)

    def update_products_from_excell(self, data):
        check = self.__db.db_read(f'SELECT row_id FROM products', ())
        for i in data:
            try:
                i[1] = int(i[1])
                if tuple(i[0]) in check:
                    old_key = self.__db.db_read(f'SELECT key FROM products WHERE row_id = ?', (i[0], ))[0][0]
                    new_keys = ','.join(set(old_key.split(',') + i[2].split(',')))
                    self.__db.db_write(f'UPDATE products SET price = ?, key = ?, preview = ?, category = ?, description = ? WHERE row_id = {i[0]}', (i[1], new_keys, i[3], i[4], i[5]))
                else:
                    self.__db.db_write(
                        f'INSERT INTO products (photo, row_id, price, key, preview, category, description) VALUES (?, ?, ?, ?, ?, ?, ?)',
                        (open('no-photo.png', 'rb').read(), i[0], i[1], i[2], i[3], i[4], i[5]))
            except:
                pass


    def update_categories_from_excell(self, data):
        check = self.__db.db_read(f'SELECT id FROM categories', ())
        for i in data:
            if tuple(i[0]) in check:
                self.__db.db_write(f'UPDATE categories SET name = ? WHERE id = {i[0]}', (i[1], ))
            else:
                self.__db.db_write(f'INSERT INTO categories (id, name) VALUES (?, ?)', i)

    def get_preview_from_sales(self, user_id):
        products = self.__db.db_read('SELECT product, name FROM sales WHERE user_id = ? AND payment_status = ?', (user_id, True))
        return list(set(products))

    def update_subcategories_from_excell(self, data):
        check = self.__db.db_read(f'SELECT id FROM subcategories', ())
        for i in data:
            if tuple(i[0]) in check:
                self.__db.db_write(f'UPDATE subcategories SET id_categories = ?, name = ? WHERE id = {i[0]}', (i[1], i[2]))
            else:
                self.__db.db_write(f'INSERT INTO subcategories (id, id_categories, name) VALUES (?, ?, ?)', i)

    def get_categories(self):
        data = self.__db.db_read('SELECT id, name FROM categories', ())
        return data

    def get_sub_by_id_categories(self, id_categories):
        data = self.__db.db_read('SELECT id, name FROM subcategories WHERE id_categories = ?', (id_categories, ))
        return data

    def get_subcategories(self):
        data = self.__db.db_read('SELECT id, name FROM subcategories', ())
        return data

    def get_product_by_id(self, id_product):
        data = self.__db.db_read('SELECT photo, price, description FROM products WHERE row_id = ?', (id_product, ))
        return data[0]

    def get_products_preview(self, id_product):
        data = self.__db.db_read(
            'SELECT row_id, preview, price FROM products WHERE category = ?',
            (id_product,))
        return data

    def update_product(self, data, field, product_id):
        self.__db.db_write(f'UPDATE products SET {field} = ? WHERE row_id = ?', (data, product_id))

    def get_all_keys_product(self, product_id):
        data = self.__db.db_read(
            'SELECT key FROM products WHERE row_id = ?',
            (product_id, ))
        if len(data) > 0:
            return data[0][0]


    def check_product_id_exist(self, product_id):
        data = self.__db.db_read('SELECT count(*) FROM products WHERE row_id = ?', (product_id,))
        if len(data) > 0:
            if data[0][0] > 0:
                status = True
            else:
                status = False
            return status


