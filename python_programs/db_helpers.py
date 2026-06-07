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


def supplies_db_path():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), 'supplies.db')


def get_supplies_connection():
    return sqlite3.connect(supplies_db_path())


def ensure_supplies_table():
    conn = get_supplies_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS fertilizers (
            fertilizer_id INTEGER PRIMARY KEY AUTOINCREMENT,
            brand TEXT NOT NULL,
            price REAL NOT NULL,
            type TEXT NOT NULL,
            UNIQUE(brand, type)
        );
    ''')
    conn.commit()
    conn.close()


def seed_supplies_data(initial_data=None):
    ensure_supplies_table()
    if initial_data is None:
        initial_data = [
            ("GreenGrow", 22.50, "vegetable"),
            ("HarvestMax", 18.75, "flower"),
            ("SoilSafe", 15.00, "grass"),
            ("EcoBlend", 24.95, "tree"),
            ("CropBoost", 20.00, "vegetable")
        ]
    conn = get_supplies_connection()
    cursor = conn.cursor()
    for brand, price, ftype in initial_data:
        cursor.execute(
            '''
            INSERT INTO fertilizers (brand, price, type)
            VALUES (?, ?, ?)
            ON CONFLICT(brand, type) DO UPDATE SET
                price=excluded.price
            ''',
            (brand, price, ftype)
        )
    conn.commit()
    conn.close()
