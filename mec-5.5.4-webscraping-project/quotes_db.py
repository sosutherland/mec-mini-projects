import sys
import argparse
from pathlib import Path
import sqlite3
from pprint import pprint
import json

DB_PATH = Path('./quotes.db')
JSON_PATH = Path('./scrapy_mini_project/xpath-scraper-results.json')


def create() -> None:
    """Create a new database."""
    if DB_PATH.is_file():
        print('Database file already exists')
        return
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute("CREATE TABLE quote( \
                    quote_id        INTEGER PRIMARY KEY, \
                    quote_text      TEXT, \
                    quote_author    TEXT \
                )")
    cur.execute("CREATE TABLE tag( \
                    tag_id          INTEGER PRIMARY KEY, \
                    quote_id        INTEGER, \
                    tag_text        TEXT, \
                    FOREIGN KEY(quote_id) REFERENCES quote(quote_id) \
                )")
    con.close()


def store() -> None:
    """Store records to the database from a JSON file."""
    if not JSON_PATH.is_file():
        print('JSON file not found')
        return
    if not DB_PATH.is_file():
        print('Database file not found')
        return
    with open(JSON_PATH) as json_file:
        json_records = json.load(json_file)
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    quote_sql = 'INSERT INTO quote(quote_text, quote_author) VALUES(?, ?)'
    tag_sql = 'INSERT INTO tag(quote_id, tag_text) VALUES(?, ?)'
    for record in json_records:
        cur.execute(quote_sql, (record['text'], record['author']))
        quote_id = cur.lastrowid
        for tag_text in record['tags']:
            cur.execute(tag_sql, (quote_id, tag_text))
    con.commit()
    con.close()


def query(statment: str) -> None:
    """Query the database with a sql <statement>."""
    if not DB_PATH.is_file():
        print('Database file not found')
        return
    con = sqlite3.connect(DB_PATH)
    pprint(con.cursor().execute(statment).fetchall())
    con.close()


def main() -> int:
    """Parse the command-line arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--create', action='store_true',
                        help='create a new database')
    parser.add_argument('-s', '--store', action='store_true',
                        help='store records to the database from a JSON file')
    parser.add_argument('-q', metavar='<statement>',
                        help='query the database with a sql <statement>')
    args = parser.parse_args()
    if args.create:
        create()
    elif args.store:
        store()
    elif args.q:
        query(args.q)
    else:
        parser.print_help()
    return 0


if __name__ == '__main__':
    sys.exit(main())
