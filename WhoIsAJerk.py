import logging

from aiogram import Bot, Dispatcher, executor, types
from scheduler import Scheduler

from bd import BaseDataRequests
from bot import (KEYBOARDS, check_bot_admin, check_group,
                 get_difference_day, get_now_date, get_random_rank,
                 plus_count_request)
from settings import API_TOKEN, TIMEZONES, TZ_SERVER
from settings.variables import ADMIN_GROUP_ID, ADMIN_ID
from ujson import dumps
from os import remove as os_remove

logging.basicConfig(level=logging.INFO)
db_requests = BaseDataRequests()

bot_api = Bot(token=API_TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot_api)
BOT_ID = API_TOKEN.split(":")[0]
schedule = Scheduler(tzinfo=TZ_SERVER)


async def set_default_commands(dp):
    await dp.bot.set_my_commands(
        [
            types.BotCommand('rank', 'Твой ранг на сегодня'),
            types.BotCommand('start', 'Приветственное сообщение'),
            types.BotCommand('set_timezone', 'Настройка таймзоны'),
            types.BotCommand('join_game', 'Присоединиться к игре'),
            types.BotCommand('secret', 'Секрет... Лучше не нажимать'),
            types.BotCommand('help', 'Помощь'),
        ]
    )


@dp.message_handler(content_types=[types.ContentType.NEW_CHAT_MEMBERS])
async def new_members_handler(message: types.Message):
    new_member = message.new_chat_members[0]

    if new_member.id == int(BOT_ID):
        await message.answer(
            db_requests.get('frazes', ['text_fraze'], 'action="secret"')
        )
        return

    await message.answer(
        db_requests.get('frazes', ['text_fraze'], action='"new_member"')
    )


@dp.message_handler(commands='start')
async def start(message: types.Message):
    plus_count_request(db_requests)
    exists = db_requests.get(
        'groups', where=f'id_group={message.chat.id}', exists=True
    )
    fraze = 'start_again' if exists else 'start'
    text = db_requests.get(
        'frazes', ['text_fraze'], f'action="{fraze}"'
    )

    await message.answer(
        text, reply_markup=KEYBOARDS['start'] if not exists else None
    )


async def set_timezone(message: types.Message, user: types.User):
    plus_count_request(db_requests)
    admins = await check_bot_admin(
        bot_api, message, db_requests, True, user.id
    )
    if not admins['bot']:
        return

    if not admins['user']:
        await message.answer(
            db_requests.get(
                'frazes', ['text_fraze'], 'action="set_timezone_not_admin"'
            )
        )
        return

    await check_group(
        message, db_requests, fraze_exist='set_timezone_again',
        fraze_none='set_timezone',
        keyboard_exist=KEYBOARDS['set_timezone'],
        keyboard_none=KEYBOARDS['set_timezone']
    )


@dp.message_handler(commands='set_timezone')
async def set_timezone_command(message: types.Message):
    await set_timezone(message, message.from_user)


@dp.callback_query_handler(text='set_timezone')
async def set_timezone_query(callback_query: types.CallbackQuery):
    await set_timezone(callback_query.message, callback_query.from_user)


@dp.callback_query_handler(text=[f'timezone_btn_{i}' for i in range(1, 12)])
async def set_timezone_btn(callback_query: types.CallbackQuery):
    plus_count_request(db_requests)
    group_id = callback_query.message.chat.id
    message = callback_query.message
    bot_is_admin = await check_bot_admin(bot_api, message, db_requests)
    if not bot_is_admin:
        return

    message_id = message.message_id
    timezone = TIMEZONES[int(callback_query.data.split('_')[-1])][0]

    group = db_requests.get(
        'groups', where=f'id_group={message.chat.id}', exists=True
    )
    if not group:
        text = db_requests.get(
            'frazes', ['text_fraze'], 'action="set_timezone_done"'
        ).format(timezone=timezone)
        db_requests.insert_group(group_id, timezone)
    else:
        db_requests.update_group(group_id, timezone=timezone)
        players = db_requests.get(
            'users', ['mention', 'summ_ball'], f'group_id={message.chat.id}',
            'summ_ball DESC', True
        )
        players = '\n'.join(
            list(
                f'{i+1}. {players[i]["mention"]} - '
                f'{players[i]["summ_ball"]}б.' for i in range(len(players))
            )
        )
        text = db_requests.get(
            'frazes', ['text_fraze'], 'action="set_timezone_done_again"'
        ).format(timezone=timezone, players=players)  \
            if players is not None else db_requests.get(
                'frazes', ['text_fraze'],
                'action="set_timezone_done_again_none_players"'
        ).format(timezone=timezone)

    await bot_api.delete_message(group_id, message_id)
    await message.answer(text, reply_markup=KEYBOARDS['join_game'])


async def join_game(message: types.Message, user: types.User):
    plus_count_request(db_requests)
    group_id = message.chat.id
    group = await check_group(message, db_requests, True)
    bot_is_admin = await check_bot_admin(
        bot_api, message, db_requests, user_id=user.id
    )

    if not bot_is_admin:
        return
    if not group['result']:
        return
    user_exists = db_requests.get(
        'users', where=f'user_id={user.id} and group_id={group_id}',
        exists=True
    )
    if user_exists:
        await message.answer(
            db_requests.get(
                'frazes', ['text_fraze'], 'action="join_game_again"'
            )
        )
        return

    group = group['group']
    date = get_now_date(group['timezone'])
    rank = get_random_rank(db_requests)
    ball = int(rank['ball'])
    ball = f'+{ball}' if ball > 0 else f'{ball}'

    db_requests.insert_user(
        user.mention, user.id, int(group['id_group']), int(rank['ball']),
        date, rank['id']
    )
    await message.answer(
        db_requests.get(
            'frazes', ['text_fraze'], 'action="join_game"'
        ).format(
            mention=user.mention, rank=rank['rank'], ball=ball, id=user.id
        )
    )


@dp.callback_query_handler(text='join_game')
async def join_game_query(callback_query: types.CallbackQuery):
    await join_game(callback_query.message, callback_query.from_user)


@dp.message_handler(commands='join_game')
async def join_game_command(message: types.Message):
    await join_game(message, message.from_user)


@dp.message_handler(commands='rank')
async def rank(message: types.Message):
    plus_count_request(db_requests)
    group_id = message.chat.id
    group = await check_group(message, db_requests, True)
    bot_is_admin = await check_bot_admin(bot_api, message, db_requests)
    user_id = message.from_user.id

    if not bot_is_admin:
        return
    if not group['result']:
        return
    user_exists = db_requests.get(
        'users', where=f'user_id={user_id} and group_id={group_id}',
        exists=True
    )
    if not user_exists:
        await message.answer(
            db_requests.get(
                'frazes', ['text_fraze'], 'action="member_not_in_game"'
            )
        )
        return

    timezone = db_requests.get(
        'groups', ['timezone'], f'id_group={group_id}'
    )
    user = db_requests.get(
        'users', ['last_appeal_to_rank', 'summ_ball', 'rank'],
        f'user_id={user_id} and group_id={group_id}'
    )

    date = user['last_appeal_to_rank']
    difference, date_today = get_difference_day(date, timezone)
    if difference > 0:
        rank = get_random_rank(db_requests)
        summ_ball = int(user['summ_ball']) + int(rank['ball'])
        db_requests.update_user(
            user_id, group_id, rank=rank['id'], last_appeal_to_rank=date_today,
            summ_ball=summ_ball
        )
    else:
        rank = db_requests.get(
            'ranks', ['ball', 'rank'], f'id={int(user["rank"])}'
        )
        if rank is None:
            message.answer(
                db_requests.get(
                    'frazes', ['text_fraze'], 'action="ooops"'
                )
            )
            return

    ball = int(rank['ball'])
    ball = f'+{ball}' if ball > 0 else f'{ball}'

    await message.answer(
        db_requests.get(
            'frazes', ['text_fraze'], 'action="rank"'
        ).format(
            id=user_id, mention=message.from_user.mention, rank=rank['rank'],
            ball=ball
        )
    )


@dp.message_handler(commands='help')
async def help(message: types.Message):
    plus_count_request(db_requests)
    await message.answer(
        db_requests.get(
            'frazes', ['text_fraze'], 'action="help"'
        )
    )


@dp.message_handler(commands='secret')
async def secret(message: types.Message):
    if message.chat.id not in [ADMIN_ID, ADMIN_GROUP_ID]:
        plus_count_request(db_requests)
        await message.answer(
            db_requests.get(
                'frazes', ['text_fraze'], 'action="secret"'
            )
        )
        return

    await message.answer(
        'Админ панель', reply_markup=KEYBOARDS['admin_panel']
    )


@dp.callback_query_handler(text='admin_show_ranks')
async def admin_show_ranks(callback_query: types.CallbackQuery):
    if callback_query.message.chat.id not in [ADMIN_ID, ADMIN_GROUP_ID]:
        return

    ranks = list(db_requests.get('ranks', ['*'], many=True))
    ranks = dumps(ranks, ensure_ascii=False, indent=4)

    with open('All_ranks.json', 'wb') as file:
        file.write(bytes(ranks, encoding='utf-8'))

    await callback_query.message.answer_document(
        open('All_ranks.json', 'rb'), reply_markup=KEYBOARDS['admin_panel']
    )
    os_remove('All_ranks.json')


@dp.callback_query_handler(text='admin_sql_ranks')
async def admin_sql_ranks(callback_query: types.CallbackQuery):
    if callback_query.message.chat.id not in [ADMIN_ID, ADMIN_GROUP_ID]:
        return

    ranks = list(db_requests.get('ranks', ['rank', 'ball'], many=True))
    length_ranks = len(ranks)
    sql = ['INSERT INTO ranks(rank, ball) VALUES']

    for i in range(length_ranks):
        text = f'("{ranks[i]["rank"]}", {ranks[i]["ball"]})'
        text += ',' if (i + 1) < length_ranks else ';'
        sql.append(text)
    sql = '\n'.join(sql)

    with open('All_ranks_sql.json', 'wb') as file:
        file.write(bytes(sql, encoding='utf-8'))

    await callback_query.message.answer_document(
        open('All_ranks_sql.json', 'rb'), reply_markup=KEYBOARDS['admin_panel']
    )
    os_remove('All_ranks_sql.json')


@dp.callback_query_handler(text='admin_add_rank')
async def admin_add_rank(callback_query: types.CallbackQuery):
    if callback_query.message.chat.id not in [ADMIN_ID, ADMIN_GROUP_ID]:
        return

    text = '''Чтобы добавить ранг, напиши мне в формате:

/admin_add_rangs_query
фраза_1:балл(отрицательный - "-1", положительный - "1")
фраза_2:балл
фраза_3:балл

<i><b>Указывать можно 1 или сколько влезет рангов</b></i>
'''
    await callback_query.message.answer(
        text, reply_markup=KEYBOARDS['admin_panel']
    )


@dp.message_handler(commands='admin_add_rangs_query')
async def admin_add_rangs_query(message: types.Message):
    if message.chat.id not in [ADMIN_ID, ADMIN_GROUP_ID]:
        return

    rangs = [item.split(':') for item in message.text.split('\n')[1:]]
    sql = ['INSERT INTO ranks(rank, ball) VALUES']
    data = []
    length_rangs = len(rangs)

    for i in range(length_rangs):
        if len(rangs[i]) != 2:
            await message.answer(
                'Проверь введённые значения, еблан!',
                reply_markup=KEYBOARDS['admin_panel']
            )
            return

        rank = rangs[i][0].strip()
        try:
            ball = int(rangs[i][1].strip())
        except ValueError:
            await message.answer(
                f'Что-то не так с рангом: {rank}',
                reply_markup=KEYBOARDS['admin_panel']
            )
            return

        text = f'("{rank}", {ball})'
        text += ',' if (i + 1) < length_rangs else ';'
        sql.append(text)
        data.append({'rank': rank, 'ball': ball})

    sql = '\n'.join(sql)
    data = dumps(data, ensure_ascii=False, indent=4)
    db_requests.post_request(sql)

    with open('custom_request.json', 'wb') as file:
        file.write(bytes(data, encoding='utf-8'))
    await message.answer_document(
        open('custom_request.json', 'rb'),
        caption='Выполнил запрос, но проверь данные!',
        reply_markup=KEYBOARDS['admin_panel']
    )
    os_remove('custom_request.json')


@dp.callback_query_handler(text='admin_edit_rank')
async def admin_edit_rank(callback_query: types.CallbackQuery):
    if callback_query.message.chat.id not in [ADMIN_ID, ADMIN_GROUP_ID]:
        return

    text = '''Чтобы изменить ранг, напиши мне в формате:

/admin_edit_rang_query
id_ранга:новую_фразу:новый_балл

<i><b>За раз изменить можно только один ранг!</b></i>
'''
    await callback_query.message.answer(
        text, reply_markup=KEYBOARDS['admin_panel']
    )


@dp.message_handler(commands='admin_edit_rang_query')
async def admin_edit_rang_query(message: types.Message):
    if message.chat.id not in [ADMIN_ID, ADMIN_GROUP_ID]:
        return

    rangs = [item.split(':') for item in message.text.split('\n')[1:]]

    if len(rangs) > 1:
        await message.answer(
            'Тупой?! Сказано было, что можно только один ранг изменять!',
            reply_markup=KEYBOARDS['admin_panel']
        )
        return
    if len(rangs) == 0:
        await message.answer(
            'Это наёбка? Тут нет рангов!',
            reply_markup=KEYBOARDS['admin_panel']
        )
        return

    _rank = rangs[0]
    try:
        id = int(_rank[0].strip())
        ball = int(_rank[2].strip())
    except ValueError:
        await message.answer(
            'Это наёбка? Неверно указан id или баллы',
            reply_markup=KEYBOARDS['admin_panel']
        )
        return
    rank = _rank[1].strip()

    exists_rank = db_requests.get(
        'ranks', where=f'id={id}', exists=True
    )
    if not exists_rank:
        await message.answer(
            'Ранга с таким id нет! Посмотри все ранги и там найдёшь id!',
            reply_markup=KEYBOARDS['admin_panel']
        )
        return

    data = {'id': id, 'rank': rank, 'ball': ball}
    data = dumps(data, ensure_ascii=False, indent=4)
    sql = f'''
UPDATE ranks SET
ball={ball}
rank="{rank}"
WHERE id={id}
'''
    db_requests.post_request(sql)
    with open('custom_request.json', 'wb') as file:
        file.write(bytes(data, encoding='utf-8'))
    await message.answer_document(
        open('custom_request.json', 'rb'),
        caption='Выполнил запрос, но проверь данные!',
        reply_markup=KEYBOARDS['admin_panel']
    )
    os_remove('custom_request.json')


@dp.callback_query_handler(text='admin_show_stats')
async def admin_show_stats(callback_query: types.CallbackQuery):
    if callback_query.message.chat.id not in [ADMIN_ID, ADMIN_GROUP_ID]:
        return

    users_count = db_requests.get('users', count=True)
    groups_count = db_requests.get('groups', count=True)
    now_date = get_now_date('UTC')
    requests_today = db_requests.get(
        'stat_requests', ['requests'], f'date={now_date}'
    )
    requests_today = 0 if requests_today is None else requests_today

    await callback_query.message.answer(
        '<i><b>Статистика:</b></i>\n'
        f'Количесво пользователей: {users_count}\n'
        f'Количество зарегестрированных групп: {groups_count}\n'
        f'Количество запросов за сегодня: {requests_today}',
        reply_markup=KEYBOARDS['admin_panel']
    )


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
