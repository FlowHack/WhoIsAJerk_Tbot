GET_TABLES = '''
SELECT name FROM sqlite_master WHERE type='table';
'''
CREATE_USERS = '''
CREATE TABLE IF NOT EXISTS users(
    id INT PRIMARY KEY,
    username TEXT,
    tg_id INT
)
'''

REQUESTS = {
    'GET': {
        'get_tables': GET_TABLES,
    },
    'DELETE': {},
    'CREATE': {
        'users': CREATE_USERS
    }
}
