import sqlite3

from config import DB_NAME


async def set_user(user_id: int) -> None:
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    cursor.execute('INSERT OR IGNORE INTO users (user_id) VALUES (?)', (user_id,))

    connection.commit()
    connection.close()


async def get_words() -> set[str]:
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    cursor.execute('SELECT * FROM words')
    words = set(row[1] for row in cursor.fetchall())

    connection.close()

    return words


async def add_words(user_id: int, words: set[str]) -> None:
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()



    connection.commit()
    connection.close()