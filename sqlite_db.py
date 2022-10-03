import sqlite3
import psycopg2


class BotDB:

    def __init__(self):
        self.conn = psycopg2.connect(
            database='d32hs4fk6f1rcv',
            user="ankamqkptqxuqq",
            password="782dcdd9b54c1d81dbd622fa7326703d2cfe16acaa2a4d69c07e9d385889c50d",
            host="ec2-34-252-216-149.eu-west-1.compute.amazonaws.com",
            port="5432"
        )
        self.cursor = self.conn.cursor()

    def user_exists(self, user_id):
        """Проверяем, есть ли юзер в базе"""
        self.cursor.execute("SELECT id FROM users WHERE user_id = %s", (user_id,))
        return bool(len(self.cursor.fetchall()))

    def get_user_id(self, user_id):
        """Достаем id юзера в базе по его user_id"""
        self.cursor.execute("SELECT id FROM users WHERE user_id = %s", (user_id,))
        return self.cursor.fetchone()[0]

    def add_user(self, user_id):
        """Добавляем юзера в базу"""
        self.cursor.execute("INSERT INTO users (user_id) VALUES (%s)", (user_id,))
        return self.conn.commit()

    def add_record(self, user_id, hotel_name, rating, price, photos):
        """Создаем запись о доходах/расходах"""
        self.cursor.execute("INSERT INTO records (user_id, hotel_name, rating,price, photos) VALUES (%s, %s, "
                            "%s, %s, %s)",
                            (self.get_user_id(user_id), hotel_name, rating, price, photos))

        return self.conn.commit()

    def get_records(self, user_id):
        """Получаем историю о доходах/расходах"""

        self.cursor.execute("SELECT * FROM records WHERE user_id = %s", (self.get_user_id(user_id),))
        return self.cursor.fetchall()

    def get_del_records(self, user_id):
        print(self.get_user_id(user_id))
        self.cursor.execute("""DELETE FROM records WHERE user_id = %s""", (self.get_user_id(user_id),))
        return self.conn.commit()

    def close(self):
        """Закрываем соединение с БД"""
        self.connection.close()
