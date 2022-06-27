SET_TIMEZONE = '''Эта команда предназначена для установки верной <i><b>таймзоны</b></i> группы.

Это упростит мою работу и сделает её удобней для вас.

Список возможных таймзон для России:
№1 Asia/Kamchatka - МСК+9/UTC+12
№2 Asia/Magadan - МСК+8/UTC+11
№3 Asia/Vladivostok - MSK+7/UTC+10
№4 Asia/Yakutsk - MSK+6/UTC+9
№5 Asia/Irkutsk - MSK+5/UTC+8
№6 Asia/Krasnoyarsk - MSK+4/UTC+7
№7 Asia/Omsk - MSK+3/UTC+6
№8 Asia/Yekaterinburg - MSK+2/UTC+5
№9 Europe/Saratov - MSK+1/UTC+4
№10 Europe/Moscow - MSK+0/UTC+3
№11 Europe/Kaliningrad - MSK-1/UTC+2

<i><b>Выбери кнопку с номером вашей таймзоны!</b></i>
'''
SET_TIMEZONE_RETRY = '''Что, всей группой прям переселились? Ну ок... Вот тебе список и кнопки.

Список возможных таймзон для России:
№1 Asia/Kamchatka - МСК+9/UTC+12
№2 Asia/Magadan - МСК+8/UTC+11
№3 Asia/Vladivostok - MSK+7/UTC+10
№4 Asia/Yakutsk - MSK+6/UTC+9
№5 Asia/Irkutsk - MSK+5/UTC+8
№6 Asia/Krasnoyarsk - MSK+4/UTC+7
№7 Asia/Omsk - MSK+3/UTC+6
№8 Asia/Yekaterinburg - MSK+2/UTC+5
№9 Europe/Saratov - MSK+1/UTC+4
№10 Europe/Moscow - MSK+0/UTC+3
№11 Europe/Kaliningrad - MSK-1/UTC+2

<i><b>Выбери кнопку с номером вашей таймзоны!</b></i>
'''
SET_TIMEZONE_NOT_ADMIN = '''Прости конечно, но ты тут никто! Настройки таймзоны доступны только админам!'''
START = '''Хайоу гондоны!

Данной мне богом властью я буду измерять вашу гондонность гондонометром!
Но это ещё не всё... Я позволю вам каждую неделю в воскресенье проводить опрос на звание "гондон недели"!

Для удобства нашего общения скажите мне в какой вы вообще таймзоне находитесь? Для этого выберите команду /set_timezone.
Ещё сделайте меня админом!
<i><b>Без этого я не стану на вас даже внимания обращать!</b></i>
'''
START_OLD = '''Это какая-то наёбка? Мы уже начали, дружок!

Если нужна помощь, команда <i><b>/help</b></i> в помощь!
'''
JOIN_GAME = '''{mention}, ты присоеденился к игре. Теперь ты <i><b>каждый день будешь получать дозу позитива</b></i>!

На сегодня у тебя {ball}б.
<a href="tg://user?id={id}">{rank}</a>'''
LEFT_GAME = '''{mention}, ты покинул игру!'''
JOIN_GAME_AGAIN = '''гондон, ты и так в игре!'''
LEFT_GAME_AGAIN = '''гондон, ты итак не в игре! Или тебя кикнуть нахер!?'''
WHO_IN_GAME = '''Список гондонов:
{gandons}'''
NEW_MEMBER = '''Очередной гондон прибыл!\n\n<a href="tg://user?id={id}">{mention}</a>'''
SECRET = '''Ты совсем гондон? Напиcано же, что секрет!'''
BOT_NOT_ADMIN = '''Ах ты гондон! В админы кто добавлять будет!?'''
BOT_NOT_ADMIN_AND_USER_TO = '''Ты гондон? Я должен быть админом! Да ты и сам не администртор...'''
SET_TIMEZONE_DONE = '''Я установил для вашей группы таймзону: {timezone}.

<i><b>ПОЕХАЛИ, СУЧЕНЬКА!</b></i>

Нажмите на кнопку <i><b>"Присоедениться к игре"</b></i> или введите команду <i><b>/join_game</b></i>, чтобы участвовать в этом жёстком гей порно.
'''
SET_TIMEZONE_DONE_AGAIN = '''Я установил для вашей группы таймзону: {timezone}.

Списочек уже участвующих:
{players}

Если остались те, кто не играют, но им очень хочется, то у вас есть уникальная возможность присоединиться!
Каждый кто хочет присоединиться к игре должен либо <i><b>нажать под этим сообщением соответствующую кнопку</b></i>, либо ввести команду <i><b>/join_game</b></i>.
'''
SET_TIMEZONE_DONE_AGAIN_NONE_PLAYERS = '''Я установил для вашей группы таймзону: {timezone}.

Но какого хера никто не играет? гондоны...
<i><b>Быстро все присоединились к игре!</b></i>

Каждый кто хочет присоединиться к игре должен либо <i><b>нажать под этим сообщением соответствующую кнопку</b></i>, либо ввести команду <i><b>/join_game</b></i>.
'''
PLAYERS = '''Список гондонов:
{players}
'''
PLAYERS_NONE = '''Так никто не играет! Нахер спрашивать кто играет!?

<i><b>Быстро все присоединились к игре!</b></i>

Каждый кто хочет присоединиться к игре должен либо <i><b>нажать под этим сообщением соответствующую кнопку</b></i>, либо ввести команду <i><b>/join_game</b></i>.
'''
NONE_THIS_GROUP = '''Что-то я вашу группу не знаю...

Нажмите на кнопку ниже, чтобы настроить таймзону, а после мы уже поговорим...'''
HELP = '''Не думал, что тут есть в чем нужна помощь...

Команды:
/rank - Узнать свой ранг на сегодня

/start - Тут и так всё понятно. Команда используется только при первом запуске бота. Это что-то типа приветствия

/set_timezone - Команда, которая выдаёт список таймзон, среди которых нужно выбрать часовой пояс этой группы. Это в будущем сделает игру более удобной

/join_game - Команда нужна, чтобы каждый желающий играть смог присоединиться! Эта команда нужна ещё и потому, что телега запретили ботам получать список всех пользоваелей, а иначе то как играть, если не знать список?!

/left_game - Выйти из игры. <i><b>Не стоит так поступать!</b></i>

/secret - Команда, которую вам придётся испытать самостоятельно =)

Требования:
- Оно всего одно: Бот должен быть админом группы и должен иметь все права)

P.S. Никто никого не оскорбляет. Бот не создан с целью унижения! Это просто игра =)'''
MEMBER_NOT_IN_GAME = '''Так ты не в игре, гондон!

Нажмите на кнопку <i><b>"Присоедениться к игре"</b></i> или введите команду <i><b>/join_game</b></i>, чтобы участвовать в этом жёстком гей порно.
'''
RANK = '''{mention}, сегодня у тебя {ball}б.
<a href="tg://user?id={id}">{rank}</a>'''
OOOPS = '''Что-то пошло не так... Попробуй позже!'''
LEFT_GAME = '''Очень жаль... <a href="tg://user?id={id}">{mention}</a>'''

DEFAULT_RESPONSES = {
    'set_timezone': SET_TIMEZONE,
    'set_timezone_not_admin': SET_TIMEZONE_NOT_ADMIN,
    'set_timezone_again': SET_TIMEZONE_RETRY,
    'set_timezone_done': SET_TIMEZONE_DONE,
    'set_timezone_done_again': SET_TIMEZONE_DONE_AGAIN,
    'set_timezone_done_again_none_players': SET_TIMEZONE_DONE_AGAIN_NONE_PLAYERS,
    'start': START,
    'start_again': START_OLD,
    'join_game': JOIN_GAME,
    'join_game_again': JOIN_GAME_AGAIN,
    'left_game': LEFT_GAME,
    'left_game_again': LEFT_GAME_AGAIN,
    'who_in_game': WHO_IN_GAME,
    'new_member': NEW_MEMBER,
    'secret': SECRET,
    'bot_not_admin': BOT_NOT_ADMIN,
    'bot_not_admin_and_user_to': BOT_NOT_ADMIN_AND_USER_TO,
    'players': PLAYERS,
    'players_none': PLAYERS_NONE,
    'none_this_group': NONE_THIS_GROUP,
    'help': HELP,
    'member_not_in_game': MEMBER_NOT_IN_GAME,
    'rank': RANK,
    'ooops': OOOPS,
}
