#!./venv/bin/python


import re
from time import localtime

from aiogram import Bot, types
from aiogram.utils import executor
from aiogram.dispatcher import Dispatcher

from config import TOKEN
from db_connection import select_word_translation
from parser import get_translation
from constants import *


bot = Bot(token=TOKEN)
disp = Dispatcher(bot)


@disp.message_handler(commands='start')
async def start_command(message: types.Message):
    await message.answer(
        f'Привет!\nВведи слово:\n(для справки введи /help)')


@disp.message_handler(commands='help')
async def help_command(message: types.Message):
    await message.answer(f'''
    Я использую онлайн словарь wordhunt.ru,\nи перевожу введённое русское слово на английский,
а введённое английское слово на русский.\n\nВводи слово, не томи :)''')


@disp.message_handler()
async def main_command(message: types.Message):
    word = message.text.lower().strip()

    try:
        if re.match(r'[а-я]', word):
            from_language = RU
        else:
            from_language = EN

        try:
            if re.match(r'[а-я]', word):
                translation = select_word_translation(word, from_language)[1]
            else:
                translation = ' '.join(list(select_word_translation(word, from_language)[1:]).reverse())

            # print(translation)
        except TypeError:
            translation = get_translation(word)

        await message.reply(translation)

    except Exception as error:
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

if __name__ == '__main__':
    # для локалки
    # with open('/home/daniil/Documents/Python/Telegram_bots/Translator_RU_EN_RU_Bot/bot_state', 'a') as bot_state:
    # для сервака
    with open('./bot_state', 'w') as bot_state:
        now_time = localtime()

        bot_state.write('Start in\n')
        # для локалки
        # bot_state.write(f' {now_time.tm_hour}.{now_time.tm_min}.{now_time.tm_sec}\n')
        # для сервака
        bot_state.write(f'Time: {now_time.tm_hour + 3}.{now_time.tm_min}.{now_time.tm_sec}\n')
	bot_state.write(f'Date: {now_time.tm_mday}.{now_time.tm_mon}.{now_time.tm_year}\n')

    executor.start_polling(disp)
