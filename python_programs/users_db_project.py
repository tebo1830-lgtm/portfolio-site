"""Grouped Users DB project: create the database, seed users, and display stored records."""

from createDB import main as create_db_main
from insert_recs import main as insert_recs_main
from show_records import showRecords as show_records_main


def main():
    print('Starting Users DB grouped project...')
    create_db_main()
    insert_recs_main()
    print('\nShowing current records:')
    show_records_main()


if __name__ == '__main__':
    main()
