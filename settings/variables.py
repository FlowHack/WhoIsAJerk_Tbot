from os import environ

DEBUG = True
API_TOKEN = environ.get('TG_API_TOKEN_DEBUG') if DEBUG  \
    else environ.get('TG_API_TOKEN')
DB_HOST = environ.get('DB_HOST')
DB_USER = environ.get('POSTGRES_USER')
DB_PASSWORD = environ.get('POSTGRES_PASSWORD')
DB_NAME = environ.get('DB_NAME')
DB_PORT = environ.get('DB_PORT')
ADMIN_ID = environ.get('ADMIN_ID')
