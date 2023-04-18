from time import localtime
import sqlite3

import asyncio
import aiosqlite
import aiofiles

from constants import RU, EN, PROJECT_PATH, TIME_ZONE, DATABASE


# ошибка при нахождении слова в таблице
class DoesNotExistWord(Exception):
    pass


# очистить всю таблицу "table"
async def clear_table(database: str, table: str) -> None:
    query = f'DELETE FROM {table};'

    try:
        # подключение к БД
        async with aiosqlite.connect(database) as con:
            # выполнение запроса query
            await con.execute(sql=query)
            # сохранение изменений
            await con.commit()
    except sqlite3.OperationalError:
        print('Sorry, there was the error')


# получить все записи из таблицы "table"
async def show_all(database:str, table: str) -> list:
    query = f'''
        SELECT * FROM {table};'''

    try:
        # подключение к БД
        async with aiosqlite.connect(database) as con:
            # выполнение запроса query
            async with con.execute(sql=query) as cursor:
                all_notes = await cursor.fetchall()
                return all_notes
    except sqlite3.OperationalError:
        print(f'Ha-ha-ha, table "{table}" is empty!')


# найти перевод слова "word" из языка "from_language" в БД
async def select_word_translation(database:str, word: str, from_language: str) -> tuple:
    query = f'''
        SELECT * FROM {from_language}
        WHERE word="{word}";'''

    try:
        # подключение к БД
        async with aiosqlite.connect(database) as con:
            # выполнение запроса query
            async with con.execute(sql=query) as cursor:
                select_word = await cursor.fetchone()

                # если слово не было найдено
                if not select_word:
                    raise DoesNotExistWord
                # возвращаем найденное слово
                return select_word

    except DoesNotExistWord:
        # print("This word haven't been found")

        async with aiofiles.open(f'{PROJECT_PATH}/bot_state.txt', 'a') as bot_state:
            now_time = localtime()

            await bot_state.write(f'''Not found "{word}" in table "{from_language}"''')
            await bot_state.write(f' (time is {now_time.tm_hour + TIME_ZONE}.{now_time.tm_min}.{now_time.tm_sec})\n\n')

        return tuple()

    except Exception as error:
        print(f'Ha-ha-ha, you caught the error in project "Translator_RU_EN_RU_Bot", in file "db_connection", in coroutine "select_word_translation": {error}')

        async with aiofiles.open(f'{PROJECT_PATH}/bot_state.txt', 'a') as bot_state:
            now_time = localtime()

            await bot_state.write(str(error))
            await bot_state.write(f' (time is {now_time.tm_hour + TIME_ZONE}.{now_time.tm_min}.{now_time.tm_sec})\n\n')

        return tuple()


# добавить перевод "translation" слова "word" из языка "from_language" (если язык 'english', то ещё добавляем transcription)
async def add_word_translation(database: str, word: str, from_language: str, translation: str, transcription: str = None) -> None:
    if from_language == RU:
        query = f'''
            INSERT OR IGNORE INTO {from_language} (word, translation)
            VALUES ('{word}', '{translation}')'''
    elif from_language == EN:
        query = f'''
            INSERT OR IGNORE INTO {from_language} (word, translation, transcription)
            VALUES ("{word}", "{translation}", "{transcription}")'''

    try:
        # подключение к БД
        async with aiosqlite.connect(database) as con:
            # выполнение запроса query
            await con.execute(sql=query)
            # сохранение изменений
            await con.commit()

            # записываем в файл состояния успешное добавление нового слова
            async with aiofiles.open(f'{PROJECT_PATH}/bot_state.txt', 'a') as bot_state:
                now_time = localtime()

                await bot_state.write(f'Word "{word}" have been added into table "{from_language}"')
                await bot_state.write(f' (time is {now_time.tm_hour + TIME_ZONE}.{now_time.tm_min}.{now_time.tm_sec})\n\n')

    # если такой таблицы в БД не найдено
    except UnboundLocalError:
        async with aiofiles.open(f'{PROJECT_PATH}/bot_state.txt', 'a') as bot_state:
            now_time = localtime()

            await bot_state.write(f'Table "{from_language}" does not exist!')
            await bot_state.write(f' (time is {now_time.tm_hour + TIME_ZONE}.{now_time.tm_min}.{now_time.tm_sec})\n\n')


# if __name__ == '__main__':
#     translation = asyncio.run(
#         select_word_translation(database=DATABASE, word='apple', from_language=EN)
#     )
#     print('translation:', translation, '\n')
#
#     asyncio.run(
#         add_word_translation(database=DATABASE, word='яма', from_language=RU, translation='то же, что something')
#     )
