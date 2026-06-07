"""Interactive Users DB project: create the DB, seed users, add/update users, and show current records."""

from createDB import main as create_db_main
from insert_recs import main as insert_recs_main
from show_records import showRecords as show_records_main
from db_helpers import get_connection, ensure_users_table


def add_or_update_user():
    try:
        raw_id = input('Enter user ID to add/update (leave blank for auto next ID): ').strip()
        user_id = int(raw_id) if raw_id else None
    except ValueError:
        print('User ID must be an integer.')
        return
    username = input('Enter username: ').strip()
    if not username:
        print('Username is required.')
        return
    password = input('Enter password: ').strip()
    if not password:
        print('Password is required.')
        return
    try:
        auth_level = int(input('Enter auth level (integer): ').strip())
    except ValueError:
        print('Auth level must be an integer.')
        return

    ensure_users_table()
    conn = get_connection()
    cursor = conn.cursor()
    if user_id is None:
        cursor.execute('SELECT MAX(user_id) FROM users')
        max_id = cursor.fetchone()[0] or 0
        user_id = max_id + 1

    cursor.execute(
        '''
        INSERT INTO users (user_id, username, password, auth_level)
        VALUES (?, ?, ?, ?)
        ON CONFLICT(user_id) DO UPDATE SET
            username=excluded.username,
            password=excluded.password,
            auth_level=excluded.auth_level
        ''',
        (user_id, username, password, auth_level)
    )
    conn.commit()
    conn.close()
    print(f'User {username} saved with user_id {user_id}.')


def show_menu():
    print('\nUsers DB Project Menu:')
    print('1. Ensure DB and users table exists')
    print('2. Seed default users')
    print('3. Add or update a user')
    print('4. Show current users')
    print('5. Exit')


def main():
    print('Starting Users DB grouped project...')
    while True:
        show_menu()
        selection = input('Choose an option: ').strip()
        if selection == '1':
            create_db_main()
        elif selection == '2':
            insert_recs_main()
        elif selection == '3':
            add_or_update_user()
        elif selection == '4':
            print('\nShowing current records:')
            show_records_main()
        elif selection == '5':
            print('Goodbye.')
            break
        else:
            print('Please select a valid option.')


if __name__ == '__main__':
    main()
