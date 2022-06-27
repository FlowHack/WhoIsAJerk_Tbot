from collections import Counter
from sqlite3 import connect as db_connect_debug

from psycopg2 import connect as db_connect

from settings import DB_HOST, DB_NAME, DB_PASSWORD, DB_PORT, DB_USER, DEBUG

from .sql import REQUESTS


class BaseData:
    def __init__(self):
        self.tables = {
            'groups': ['id', 'id_group', 'timezone', 'week_gondon'],
            'users': [
                'id', 'mention', 'user_id', 'group_id',
                'summ_ball', 'last_appeal_to_rank', 'rank'
            ],
            'ranks': ['id', 'rank', 'ball'],
            'frazes': ['id', 'action', 'text_fraze'],
            'stat_requests': ['id', 'date', 'requests']
        }
        self.connect = db_connect_debug('bd.sqlite') if DEBUG else db_connect(
            host=DB_HOST, user=DB_USER, password=DB_PASSWORD,
            dbname=DB_NAME, port=DB_PORT
        )
        self.cursor = self.connect.cursor()

        self.check_tables()

    def check_tables(self):
        self.cursor.execute(REQUESTS['GET']['tables'])
        tables = [item[0] for item in self.cursor.fetchall()]
        create = Counter(list(self.tables.keys())) - Counter(tables)

        if len(create) > 0:
            self.create_tabels(create)

    def create_tabels(self, names):
        for name in names:
            self.cursor.execute(REQUESTS['CREATE'][name])
            self.connect.commit()
            if name in REQUESTS['INSERT'].keys():
                self.cursor.execute(REQUESTS['INSERT'][name])
                self.connect.commit()
