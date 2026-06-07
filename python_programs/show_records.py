"""Users DB project: display all records from the shared people.db users table."""

from db_helpers import ensure_users_table, get_connection


def showRecords():
    ensure_users_table()
    title = "All Records From the Table Users:"
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users ORDER BY user_id")
    rows = cursor.fetchall()
    print(title)
    if not rows:
        print("No records found.")
    for row in rows:
        print(f"{row[0]} {row[1]} {row[2]} {row[3]}")
    conn.close()


if __name__ == '__main__':
    showRecords()