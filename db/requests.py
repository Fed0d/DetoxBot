import sqlite3

from config import DB_NAME


async def set_user(user_id: int) -> None:
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    cursor.execute('INSERT OR IGNORE INTO users (user_id) VALUES (?)', (user_id,))

    connection.commit()
    connection.close()


async def get_words(user_id: int) -> set[str]:
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    cursor.execute('SELECT * FROM words')
    words = set(row[1] for row in cursor.fetchall())

    cursor.execute('SELECT word FROM user_removed_words WHERE user_id = ?', (user_id,))
    removed_words = set(row[0] for row in cursor.fetchall())

    cursor.execute('SELECT word FROM user_added_words WHERE user_id = ?', (user_id,))
    added_words = set(row[0] for row in cursor.fetchall())

    words = words - removed_words
    words = words.union(added_words)

    connection.close()

    return words


async def set_added_user_words(user_id: int, words: set[str]) -> None:
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    for word in words:
        word = word.lower()
        cursor.execute('SELECT (?) FROM words', (word,))
        result = cursor.fetchone()
        if result is not None:
            cursor.execute('INSERT OR IGNORE INTO user_added_words (user_id, word) VALUES (?, ?)', (user_id, word))

    connection.commit()
    connection.close()


async def set_removed_user_words(user_id: int, words: set[str]) -> None:
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    for word in words:
        word = word.lower()
        cursor.execute('SELECT word FROM words WHERE word = ?', (word,))
        word_in_db = cursor.fetchone()
        if word_in_db is not None:
            cursor.execute('INSERT OR IGNORE INTO user_removed_words (user_id, word) VALUES (?, ?)',
                           (user_id, word))
        else:
            cursor.execute('SELECT word FROM user_added_words WHERE user_id = ? AND word = ?', (user_id, word))
            word_in_added = cursor.fetchone()
            if word_in_added is not None:
                cursor.execute('DELETE FROM user_added_words WHERE user_id = ? AND word = ?', (user_id, word))

    connection.commit()
    connection.close()


async def get_added_user_words(user_id: int) -> set[str]:
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    cursor.execute('SELECT word FROM user_added_words WHERE user_id = ?', (user_id,))
    added_words = set(row[0] for row in cursor.fetchall())

    words = added_words

    connection.close()

    return words


async def get_removed_user_words(user_id: int) -> set[str]:
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    cursor.execute('SELECT word FROM user_removed_words WHERE user_id = ?', (user_id,))
    removed_words = set(row[0] for row in cursor.fetchall())

    words = removed_words

    connection.close()

    return words
