import datetime
import sqlite3

CREATE_ENTRIES_TABLE = """CREATE TABLE IF NOT EXISTS entries (
    id INTEGER PRIMARY KEY,
    entry_title TEXT,
    entry_content TEXT,
    entry_timestamp REAL
);"""
INSERT_ENTRY = "INSERT INTO entries (entry_title, entry_content, entry_timestamp) VALUES (?, ?, ?);"
SELECT_ALL_ENTRIES = "SELECT * FROM entries;"
SELECT_ENTRIES_BY_YEAR = "SELECT * FROM entries WHERE strftime('%Y', datetime(entry_timestamp, 'unixepoch')) = ?;"
SELECT_ENTRIES_BY_MONTH_YEAR = """
SELECT * FROM entries
WHERE
    strftime('%Y', datetime(entry_timestamp, 'unixepoch')) = ?
    AND strftime('%m', datetime(entry_timestamp, 'unixepoch')) = ?;
"""
SELECT_ENTRY_BY_DATE = (
    "SELECT * FROM entries WHERE entry_timestamp >= ? AND entry_timestamp < ?;"
)
SEARCH_ENTRIES = """SELECT * FROM ENTRIES WHERE (entry_content ) LIKE ?;"""


connection = sqlite3.connect("./data/data.db")


def create_tables():
    with connection:
        connection.execute(CREATE_ENTRIES_TABLE)


def add_entry(entry_title, entry_content):
    today_timestamp = datetime.datetime.today().timestamp()
    with connection:
        connection.execute(INSERT_ENTRY, (entry_title, entry_content, today_timestamp))


def get_entries():
    with connection:
        cursor = connection.cursor()
        cursor.execute(SELECT_ALL_ENTRIES)
    return cursor.fetchall()


def get_entries_by_year(year):
    with connection:
        cursor = connection.cursor()
        cursor.execute(SELECT_ENTRIES_BY_YEAR, (str(year),))
        return cursor.fetchall()


def get_entries_by_month_and_year(month, year):
    with connection:
        cursor = connection.cursor()
        cursor.execute(SELECT_ENTRIES_BY_MONTH_YEAR, (str(year), str(month).zfill(2)))
        return cursor.fetchall()


def get_entry_by_date(date):
    start_of_day = datetime.datetime.combine(date, datetime.time.min).timestamp()
    start_of_next_day = datetime.datetime.combine(
        date + datetime.timedelta(days=1), datetime.time.min
    ).timestamp()

    with connection:
        cursor = connection.cursor()
        cursor.execute(SELECT_ENTRY_BY_DATE, (start_of_day, start_of_next_day))
        return cursor.fetchall()


def search_entries(search_term):
    with connection:
        cursor = connection.cursor()
        cursor.execute(SEARCH_ENTRIES, (f"%{search_term}%",))
        return cursor.fetchall()
