from datetime import timezone
from os import environ

DEBUG = False if environ.get('DEBUG') == '0' else True
API_TOKEN = environ.get('TG_API_TOKEN_DEBUG') if DEBUG  \
    else environ.get('TG_API_TOKEN')
DB_HOST = environ.get('DB_HOST')
DB_USER = environ.get('POSTGRES_USER')
DB_PASSWORD = environ.get('POSTGRES_PASSWORD')
DB_NAME = environ.get('DB_NAME')
DB_PORT = environ.get('DB_PORT')
ADMIN_ID = int(environ.get('ADMIN_ID'))
ADMIN_GROUP_ID = int(environ.get('ADMIN_GROUP_ID'))
TZ_SERVER = timezone.utc

TIMEZONES = {
    1: ['Asia/Kamchatka', 'МСК+9/UTC+12'],
    2: ['Asia/Magadan', 'МСК+8/UTC+11'],
    3: ['Asia/Vladivostok', 'MSK+7/UTC+10'],
    4: ['Asia/Yakutsk', 'MSK+6/UTC+9'],
    5: ['Asia/Irkutsk', 'MSK+5/UTC+8'],
    6: ['Asia/Krasnoyarsk', 'MSK+4/UTC+7'],
    7: ['Asia/Omsk', 'MSK+3/UTC+6'],
    8: ['Asia/Yekaterinburg', 'MSK+2/UTC+5'],
    9: ['Europe/Saratov', 'MSK+1/UTC+4'],
    10: ['Europe/Moscow', 'MSK+0/UTC+3'],
    11: ['Europe/Kaliningrad', 'MSK-1/UTC+2'],
}
