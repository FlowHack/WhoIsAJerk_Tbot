from .main import BaseData
from .sql import REQUESTS


class BaseDataRequests(BaseData):
    def __init__(self):
        super().__init__()
        self.requests_update = REQUESTS['UPDATE']

    def get(self, table: str, select: list[str] = ['id'], where: str = None,
            order_by: str = None, many: bool = False,
            exists: bool = False, count: bool = False):
        select_str = ', '.join(select)
        request = [f'SELECT {select_str}', f'FROM {table}']
        if where is not None:
            request.append(f'WHERE {where}')
        if order_by is not None:
            request.append(f'ORDER BY {order_by}')
        request = '\n'.join(request)

        self.cursor.execute(request)

        if exists:
            result = self.cursor.fetchone()
            return True if result is not None else False
        if count:
            return len(self.cursor.fetchone())

        columns = self.tables[table] if select_str == '*' else select
        if not many:
            result = self.cursor.fetchone()
            if result is None:
                return

            result = {columns[i]: result[i] for i in range(len(columns))}  \
                if len(columns) > 1 else result[0]
        else:
            result = self.cursor.fetchall()
            if len(result) == 0:
                return
            result = [
                {
                    columns[i]: item[i] for i in range(len(columns))
                } for item in result
            ]

        return result

    def insert_group(self, id_group: int, timezone: str, members: str = None,
                     week_gondon: str = None):

        members = 'null' if members is None else str('"' + members + '"')
        week_gondon = 'null' if week_gondon is None else week_gondon
        request = f'''
INSERT INTO groups(id_group, timezone, week_gondon)
VALUES({id_group}, "{timezone}", {week_gondon});
'''
        self.cursor.execute(request)
        self.connect.commit()

    def insert_user(self, mention: str, user_id: int, group_id: int,
                    summ_ball: int, last_appeal_to_rank: str, rank: str):
        request = f'''
INSERT INTO users(mention, user_id, group_id, summ_ball, last_appeal_to_rank, rank)
VALUES("{mention}", {user_id}, {group_id}, {summ_ball}, "{last_appeal_to_rank}", "{rank}");
'''
        self.cursor.execute(request)
        self.connect.commit()

    def update_group(self, group_id: int, timezone: str = None,
                     week_gondon: int = None):
        request = self.requests_update['group']

        variables = []
        if timezone is not None:
            variables.append(f'timezone="{timezone}"')
        if week_gondon is not None:
            variables.append(f'week_gondon={week_gondon}')

        self.cursor.execute(
            request.format(id_group=group_id, variables=',\n'.join(variables))
        )
        self.connect.commit()

    def update_user(self, user_id, group_id: int, mention: str = None,
                    summ_ball: int = None, last_appeal_to_rank: str = None,
                    rank: int = None):
        request = self.requests_update['user']

        variables = []
        if mention is not None:
            variables.append(f'mention="{mention}"')
        if summ_ball is not None:
            variables.append(f'summ_ball={summ_ball}')
        if last_appeal_to_rank is not None:
            variables.append(f'last_appeal_to_rank="{last_appeal_to_rank}"')
        if rank is not None:
            variables.append(f'rank="{rank}"')

        self.cursor.execute(
            request.format(
                user_id=user_id, group_id=group_id,
                variables=',\n'.join(variables)
            )
        )
        self.connect.commit()

    def update_stat_requests(self, date, requests):
        request = self.requests_update['stat_requests'].format(
            date=date, requests=requests
        )
        self.cursor.execute(request)
        self.connect.commit()

    def post_request(self, request):
        self.cursor.execute(request)
        self.connect.commit()
