from db_helpers import ensure_users_table, get_connection
from users import users



def main():
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
    print("Data inserted successfully.")


if __name__ == '__main__':
    main()