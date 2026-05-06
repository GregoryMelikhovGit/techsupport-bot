import sqlite3
from config import DATABASE

class DB_Manager:
    def __init__(self, database):
        self.database = database
    def create_tables(self):
        conn = sqlite3.connect(self.database)
        with conn:
            conn.execute('''CREATE TABLE IF NOT EXISTS questions (
                         question_id INTEGER,
                         question TEXT,
                         answer TEXT)''')
            conn.execute('''CREATE TABLE IF NOT EXISTS depts (
                         dept_id INTEGER PRIMARY KEY,
                         dept_name TEXT)''')
            conn.execute('''CREATE TABLE IF NOT EXISTS requests (
                         request_id INTEGER PRIMARY KEY,
                         request TEXT,
                         user_id INTEGER,
                         dept_id INTEGER,
                         FOREIGN KEY(dept_id) REFERENCES depts(dept_id))''')
            conn.commit() 
        print("База данных успешно создана!")
    def fill_tables(self):
        conn = sqlite3.connect(self.database)
        cur = conn.cursor()
        cur.execute('''INSERT INTO questions VALUES 
                    (1, 'Как оформить заказ?', 'Для оформления заказа, пожалуйста, выберите интересующий вас товар и нажмите кнопку "Добавить в корзину", затем перейдите в корзину и следуйте инструкциям для завершения покупки.'),
                    (2, 'Как узнать статус моего заказа?', 'Вы можете узнать статус вашего заказа, войдя в свой аккаунт на нашем сайте и перейдя в раздел "Мои заказы". Там будет указан текущий статус вашего заказа.'),
                    (3, 'Как отменить заказ?', 'Если вы хотите отменить заказ, пожалуйста, свяжитесь с нашей службой поддержки как можно скорее. Мы постараемся помочь вам с отменой заказа до его отправки.'),
                    (4, 'Что делать, если товар пришел поврежденным?', 'При получении поврежденного товара, пожалуйста, сразу свяжитесь с нашей службой поддержки и предоставьте фотографии повреждений. Мы поможем вам с обменом или возвратом товара.'),
                    (5, 'Как связаться с вашей технической поддержкой?', 'Вы можете связаться с нашей технической поддержкой через телефон на нашем сайте или написать нам в чат-бота.'),
                    (6, 'Как узнать информацию о доставке?', 'Информацию о доставке вы можете найти на странице оформления заказа на нашем сайте. Там указаны доступные способы доставки и сроки.')
                    ''')
        cur.execute('''INSERT INTO depts VALUES
                    (1, 'Отдел разработки'),
                    (2, 'Отдел продаж')
                    ''')
        conn.commit()
    def __executemany(self, sql, data):
        conn = sqlite3.connect(self.database)
        with conn:
            conn.executemany(sql, data)
            conn.commit()
    def insert_request(self, data):
        sql = 'INSERT OR IGNORE INTO requests (request, user_id, dept_id) values(?, ?, ?)'
        self.__executemany(sql, data)
    def get_questions(self):
        conn = sqlite3.connect(self.database)
        sql = 'SELECT question FROM questions'
        with conn:
            cur = conn.cursor()
            cur.execute(sql)
            return [row[0] for row in cur.fetchall()]
    def get_answers(self):
        conn = sqlite3.connect(self.database)
        sql = 'SELECT answer FROM questions'
        with conn:
            cur = conn.cursor()
            cur.execute(sql)
            return [row[0] for row in cur.fetchall()]
    def get_depts(self):
        conn = sqlite3.connect(self.database)
        sql = 'SELECT dept_name FROM depts'
        with conn:
            cur = conn.cursor()
            cur.execute(sql)
            return [row[0] for row in cur.fetchall()]



if __name__ == '__main__':
    manager = DB_Manager(DATABASE)
    manager.create_tables()
    manager.fill_tables()