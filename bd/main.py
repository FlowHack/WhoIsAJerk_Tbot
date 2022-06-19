from psycopg2 import connect as db_connect
from os import environ
from settings import DEBUG, DB_PASSWORD, DB_HOST, DB_NAME, DB_PORT, DB_USER, ADMIN_ID
from sqlite3 import connect as db_connect_debug
from .requests import REQUESTS
from collections import Counter


class BaseData:
    def __init__(self, bot):
        self.bot = bot
        self.tables = ['users']
        self.connect = db_connect_debug('bd.sqlite') if DEBUG else db_connect(
            host=DB_HOST, user=DB_USER, password=DB_PASSWORD,
            dbname=DB_NAME, port=DB_PORT
        )
        self.cursor = self.connect.cursor()

        self.check_tables()

    def check_tables(self):
        self.cursor.execute(REQUESTS['GET']['get_tables'])
        tables = self.cursor.fetchall()[0]
        create = Counter(self.tables) - Counter(tables)

        if len(create) > 0:
            self.create_tabels(create)

    def create_tabels(self, names):
        for name in names:
            text = f'Создаю таблицу {name}'
            self.bot.send_message(text=text, chat_id=ADMIN_ID)
            self.cursor.execute(REQUESTS['CREATE'][name])
