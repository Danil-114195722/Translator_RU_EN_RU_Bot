#!./venv/bin/python


import re
from time import localtime

from aiogram import Bot, types
from aiogram.utils import executor
from aiogram.dispatcher import Dispatcher

import asyncio
import aiofiles

from config import TOKEN
from db_connection import select_word_translation
from parser import get_translation
from constants import RU, EN, PROJECT_PATH, TIME_ZONE, DATABASE


bot = Bot(token=TOKEN)
disp = Dispatcher(bot)


@disp.message_handler(commands='start')
async def start_command(message: types.Message) -> None:
    await message.answer(
        f'Привет!\nВведи слово:\n(для справки введи /help)')


@disp.message_handler(commands='help')
async def help_command(message: types.Message) -> None:
    await message.answer(f'''
    Я использую онлайн словарь wordhunt.ru,\nи перевожу введённое русское слово на английский, а введённое английское слово на русский.
\nДля наиболее корректного результата вводите слово в начальной форме вне зависимости от языка (если это возможно).
\nОсобое внимание обратите на начальные формы этих частей речи русского языка:
1) Имя существительное: именительный падеж, единственное число
2) Имя прилагательное: именительный падеж, единственное число, мужской род
3) Имя числительное: именительный падеж
4) Местоимение: именительный падеж, единственное число
5) Глагол: инфинитив
6) Причастие: именительный падеж, единственное число, мужской род
\nДля слов английского языка стоит упомянуть о наличии только единственного числа (для правильных существительных) и отсутствии притяжательного значения (для существительных).
\nЕсли вы ознакомились с подсказкой, то можете вводить слово''')


@disp.message_handler()
async def main_command(message: types.Message) -> None:
    word = message.text.lower().strip()

    try:
        if re.match(r'[а-я]', word):
            from_language = RU
        else:
            from_language = EN

        try:
            # выбираем запись с переводом из БД
            get_db_note = await asyncio.create_task(
                select_word_translation(database=DATABASE, word=word, from_language=from_language)
            )
            # если запись не была найдена
            if not get_db_note:
                raise TypeError
            # преобразуем выбранную запись в формат для вывода пользователю
            if re.match(r'[а-я]', word):
                translation = get_db_note[1]
            else:
                translation = ' '.join(list(get_db_note[-1::-1]))

        # если запись с переводом не найдена в БД
        except TypeError:
            translation = await asyncio.create_task(get_translation(word))

        await message.reply(translation)

    except Exception as error:
        async with aiofiles.open(f'{PROJECT_PATH}/bot_state.txt', 'a') as bot_state:
            now_time = localtime()

            await bot_state.write(str(error))
            await bot_state.write(f' {now_time.tm_hour + TIME_ZONE}.{now_time.tm_min}.{now_time.tm_sec}\n\n')

if __name__ == '__main__':
    with open(f'{PROJECT_PATH}/bot_state.txt', 'w') as bot_state:
        now_time = localtime()

        bot_state.write('Start at\n')
        bot_state.write(f'Time: {now_time.tm_hour + TIME_ZONE}.{now_time.tm_min}.{now_time.tm_sec}\n')
        bot_state.write(f'Date: {now_time.tm_mday}.{now_time.tm_mon}.{now_time.tm_year}\n\n')

    executor.start_polling(disp)
