import sqlite3
from sqlite3 import Connection, Error
from time import localtime

from constants import *


# выполнить SQL-команду "query"
def execute_query(con: Connection, query):
    cur = con.cursor()
    result = None

    # # проверка
    # print('This is your query:')
    # print(query + '\n')

    try:
        result = cur.execute(query)
        con.commit()

        # # проверка
        # print('Done!')

    except Error as error:
        print(f'Ha-ha-ha, you caught the error in project "Translator_RU_EN_RU_Bot", in file "db_connection", in func "execute_query": {error}')
        # для локалки
        # with open('/home/daniil/Documents/Python/Telegram_bots/Translator_RU_EN_RU_Bot/bot_state', 'a') as bot_state:
        # для сервака
        with open('./bot_state', 'a') as bot_state:
            now_time = localtime()

            bot_state.write(error)
            # для локалки
            # bot_state.write(f' {now_time.tm_hour}.{now_time.tm_min}.{now_time.tm_sec}\n')
            # для сервака
            bot_state.write(f' {now_time.tm_hour + 3}.{now_time.tm_min}.{now_time.tm_sec}\n')
            bot_state.write('\n')

    return result


# очистить всю таблицу "table"
def clear_table(table):
    query = f'DELETE FROM {table}'
    execute_query(CONNECTION, query)


# напечатать всю таблицу "table"
def show_all(table):
    query = f'''
        select * from {table};'''
    all_notes = execute_query(CONNECTION, query)

    try:
        for note in all_notes:
            print(note)
    except TypeError:
        print(f'Ha-ha-ha, table "{table}" is empty!')


# найти перевод слова "word" из языка "from_language" в бд
def select_word_translation(word, from_language):
    query = f'''
        select * from {from_language}
        WHERE word="{word}";'''

    try:
        return tuple(execute_query(CONNECTION, query))[0]
    except IndexError:
        return None


# добавить перевод "translation" слова "word" из языка "from_language" (если язык 'english', то ещё добавляем transcription)
def add_word_translation(word, translation, transcription, from_language):
    if from_language == RU:
        query = f'''
            INSERT OR IGNORE INTO {from_language} (word, translation)
            VALUES ('{word}', '{translation}')'''
    else:
        query = f'''
            INSERT OR IGNORE INTO {from_language} (word, translation, transcription)
            VALUES ("{word}", "{translation}", "{transcription}")'''

    execute_query(CONNECTION, query)


# if __name__ == '__main__':
#     # add_word_translation('hello', 'привет, здравствуйте, приветствие', 'english')
#     # add_word_translation('привет', 'hello, hi, regards', 'russian')
#     translation = select_all_news_from_category('gg', 'english')[1]
#     print(translation)
