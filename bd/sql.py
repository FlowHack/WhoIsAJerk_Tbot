from bot import DEFAULT_RESPONSES

GET_TABLES = '''SELECT name FROM sqlite_master WHERE type="table";'''
CREATE_USERS = '''
CREATE TABLE IF NOT EXISTS users(
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    mention TEXT NOT NULL,
    user_id INTEGER NOT NULL,
    group_id INTEGER NOT NULL,
    summ_ball INTEGER NOT NULL,
    last_appeal_to_rank TEXT NOT NULL,
    rank INTEGER NOT NULL
)
'''
CREATE_GROUPS = '''
CREATE TABLE IF NOT EXISTS groups(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_group INTEGER NOT NULL,
    timezone TEXT NOT NULL,
    week_gondon INTEGER
)
'''
CREATE_FRAZES = '''
CREATE TABLE IF NOT EXISTS frazes(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    action TEXT NOT NULL,
    text_fraze TEXT NOT NULL
)
'''
INSERT_FRAZES = f'''
INSERT INTO frazes(action, text_fraze) VALUES
("set_timezone", "{DEFAULT_RESPONSES['set_timezone']}"),
("set_timezone_again", "{DEFAULT_RESPONSES['set_timezone_again']}"),
("set_timezone_not_admin", "{DEFAULT_RESPONSES['set_timezone_not_admin']}"),
("start", "{DEFAULT_RESPONSES['start']}"),
("start_again", "{DEFAULT_RESPONSES['start_again']}"),
("join_game", "{DEFAULT_RESPONSES['join_game']}"),
("join_game_again", "{DEFAULT_RESPONSES['join_game_again']}"),
("left_game", "{DEFAULT_RESPONSES['left_game']}"),
("left_game_again", "{DEFAULT_RESPONSES['left_game_again']}"),
("who_in_game", "{DEFAULT_RESPONSES['who_in_game']}"),
("new_member", "{DEFAULT_RESPONSES['new_member']}"),
("left_member", "{DEFAULT_RESPONSES['left_member']}"),
("secret", "{DEFAULT_RESPONSES['secret']}"),
("bot_not_admin", "{DEFAULT_RESPONSES['bot_not_admin']}"),
("bot_not_admin_and_user_to", "{DEFAULT_RESPONSES['bot_not_admin_and_user_to']}"),
("set_timezone_done", "{DEFAULT_RESPONSES['set_timezone_done']}"),
("set_timezone_done_again", "{DEFAULT_RESPONSES['set_timezone_done_again']}"),
("set_timezone_done_again_none_players", "{DEFAULT_RESPONSES['set_timezone_done_again_none_players']}"),
("players", "{DEFAULT_RESPONSES['players']}"),
("players_none", "{DEFAULT_RESPONSES['players_none']}"),
("none_this_group", "{DEFAULT_RESPONSES['none_this_group']}"),
("help", "{DEFAULT_RESPONSES['help']}"),
("member_not_in_game", "{DEFAULT_RESPONSES['member_not_in_game']}"),
("rank", "{DEFAULT_RESPONSES['rank']}"),
("ooops", "{DEFAULT_RESPONSES['ooops']}");
'''
CREATE_RANKS = '''
CREATE TABLE IF NOT EXISTS ranks(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    rank TEXT NOT NULL,
    ball INTEGER NOT NULL
)
'''
INSERT_RANKS = '''
INSERT INTO ranks(rank, ball) VALUES
("Гандон от БОГА", 10),
("Гандонище", 4),
("Гандон всех гандонов", 7),
("Гандонио Бандерас", 2),
("На сегодня ты чист, но рано радоваться", 0),
("Маленькими шажками ты станешь мировым гондом", 1),
("2", Растешь, рядовой гондон),
("Ну бог любит троицу, что сказать.... Гандон...", 3),
("Неплохо, но для такого гондонища могло быть и лучше", 4),
("Тут надо бы тебя оскорбить, но да ладно...", 5),
("Кличайте его Ягон Дон, великий и ужасный", 6),
("Лучше бы не нажимал...", 7)
'''
CREATE_STAT_REQUESTS = '''
CREATE TABLE IF NOT EXISTS stat_requests(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date DATE NOT NULL,
    requests INTEGER NOT NULL
)
'''
UPDATE_STAT_REQUESTS = '''
UPDATE stat_requests SET
requests={requests}
WHERE date={date}
'''
UPDATE_GROUP = '''
UPDATE groups SET
{variables}
WHERE id_group={id_group}
'''
UPDATE_USER = '''
UPDATE users SET
{variables}
WHERE user_id={user_id} and group_id={group_id}
'''

REQUESTS = {
    'GET': {
        'tables': GET_TABLES,
    },
    'DELETE': {},
    'UPDATE': {
        'group': UPDATE_GROUP,
        'user': UPDATE_USER,
        'stat_requests': UPDATE_STAT_REQUESTS
    },
    'INSERT': {
        'frazes': INSERT_FRAZES,
        'ranks': INSERT_RANKS,
    },
    'CREATE': {
        'groups': CREATE_GROUPS,
        'users': CREATE_USERS,
        'frazes': CREATE_FRAZES,
        'ranks': CREATE_RANKS,
        'stat_requests': CREATE_STAT_REQUESTS,
    }
}
