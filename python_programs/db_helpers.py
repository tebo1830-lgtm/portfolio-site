import os
import sqlite3


def db_path():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), 'people.db')


def get_connection():
    return sqlite3.connect(db_path())


def ensure_users_table():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT NOT NULL,
            password TEXT NOT NULL,
            auth_level INTEGER NOT NULL
        );
    ''')
    conn.commit()
    conn.close()


def seed_users(users):
    ensure_users_table()
    conn = get_connection()
    cursor = conn.cursor()
    for user in users:
        cursor.execute(
            '''
            INSERT INTO users (user_id, username, password, auth_level)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(user_id) DO UPDATE SET
                username=excluded.username,
                password=excluded.password,
                auth_level=excluded.auth_level
            ''',
            (user['user_id'], user['username'], user['password'], user['auth_level'])
        )
    conn.commit()
    conn.close()
