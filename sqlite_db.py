import sqlite3


class BotDB:

    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()

    def user_exists(self, user_id):
        """Проверяем, есть ли юзер в базе"""
        result = self.cursor.execute("SELECT `id` FROM `users` WHERE `user_id` = ?", (user_id,))
        return bool(len(result.fetchall()))

    def get_user_id(self, user_id):
        """Достаем id юзера в базе по его user_id"""
        result = self.cursor.execute("SELECT `id` FROM `users` WHERE `user_id` = ?", (user_id,))
        return result.fetchone()[0]

    def add_user(self, user_id):
        """Добавляем юзера в базу"""
        self.cursor.execute("INSERT INTO `users` (`user_id`) VALUES (?)", (user_id,))
        return self.conn.commit()

    def add_record(self, user_id, hotel_name, rating, price):
        """Создаем запись о доходах/расходах"""
        self.cursor.execute("INSERT INTO `records` (`user_id`, `hotel_name`, `rating`,'price') VALUES (?, ?, ?, ?)",
                            (self.get_user_id(user_id), hotel_name, rating, price))

        return self.conn.commit()

    def get_records(self, user_id):
        """Получаем историю о доходах/расходах"""

        result = self.cursor.execute("SELECT * FROM `records` WHERE `user_id` = ?", (self.get_user_id(user_id),))
        return result.fetchall()

    def get_del_records(self, user_id):
        print(self.get_user_id(user_id))
        self.cursor.execute("""DELETE FROM records WHERE user_id = ?""", (self.get_user_id(user_id),))
        return self.conn.commit()

    def close(self):
        """Закрываем соединение с БД"""
        self.connection.close()
