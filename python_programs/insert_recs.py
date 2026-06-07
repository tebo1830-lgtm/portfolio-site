import sqlite3
import os
from users import users


def db_path():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), 'people.db')


def main():
    conn = sqlite3.connect(db_path())
    cursor = conn.cursor()

    for user in users:
        cursor.execute("SELECT user_id FROM users WHERE user_id = ?", (user['user_id'],))
        if cursor.fetchone() is None:
            cursor.execute(
                "INSERT INTO users (user_id, username, password, auth_level) VALUES (?, ?, ?, ?)",
                (user['user_id'], user['username'], user['password'], user['auth_level'])
            )

    conn.commit()
    conn.close()

    print("Data inserted successfully.")


if __name__ == '__main__':
    main()