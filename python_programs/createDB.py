from db_helpers import ensure_users_table



def main():
    ensure_users_table()
    print("Database initialized and users table ensured.")

if __name__ == '__main__':
    main()