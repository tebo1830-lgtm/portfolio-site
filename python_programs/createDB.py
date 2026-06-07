import sqlite3
import os


def db_path():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), 'people.db')


def main():
    conn = sqlite3.connect(db_path())
    cursor = conn.cursor()

    # Check if the table already exists
    cursor.execute('''
        SELECT name FROM sqlite_master WHERE type='table' AND name='users';
    ''')
    table_exists = cursor.fetchone()

    if not table_exists:
        cursor.execute('''
            CREATE TABLE users (
                user_id INTEGER PRIMARY KEY,
                username TEXT NOT NULL,
                password TEXT NOT NULL,
                auth_level REAL NOT NULL
            );
        ''')
        print("Table created successfully.")
    else:
        print("Table already exists.")

    conn.commit()
    conn.close()

if __name__ == '__main__':
    main()