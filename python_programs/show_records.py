import sqlite3
import os


def db_path():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), 'people.db')


def showRecords():
    title = "All Records From the Table Users: "
    conn = sqlite3.connect(db_path())
    cursor = conn.cursor()
    sql = "SELECT * FROM users"
    cursor.execute(sql)
    rows = cursor.fetchall()
    print(title)
    for row in rows:
        print(f"{row[0]} {row[1]} {row[2]} {row[3]}")
    conn.close()


if __name__ == '__main__':
    showRecords()