import sqlite3

from config import DB_NAME, WORDS


def initialize_database():
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    cursor.execute('CREATE TABLE IF NOT EXISTS words (id INTEGER PRIMARY KEY, word TEXT UNIQUE)')
    cursor.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, user_id INTEGER UNIQUE)')
    cursor.execute('CREATE TABLE IF NOT EXISTS user_removed_words (id INTEGER PRIMARY KEY, user_id INTEGER, '
                   'word TEXT, FOREIGN KEY (user_id) REFERENCES users (user_id))')
    cursor.execute('CREATE TABLE IF NOT EXISTS user_added_words (id INTEGER PRIMARY KEY, user_id INTEGER, '
                   'word TEXT, FOREIGN KEY (user_id) REFERENCES users (user_id))')
    cursor.execute('SELECT COUNT(*) FROM words')

    count = cursor.fetchone()[0]
    if count == 0:
        with open(WORDS, 'r', encoding='UTF-8') as f:
            words = set(line.strip() for line in f)
        cursor.executemany('INSERT INTO words (word) VALUES (?)', ((word,) for word in words))

    connection.commit()
    connection.close()
