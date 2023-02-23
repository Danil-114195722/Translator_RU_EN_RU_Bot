import re
from time import localtime

from bs4 import BeautifulSoup
from fake_useragent import UserAgent

import asyncio
import aiohttp
import aiofiles

from db_connection import add_word_translation
from constants import RU, EN, PROJECT_PATH, TIME_ZONE, DEFAULT_PAGE, DATABASE


# получаем перевод слова "word"
async def get_translation(word: str) -> str:
    # ошибки для вывода пользователю
    error_not_exist_word = 'Вы неверно ввели слово! Проверьте своё написание'
    error_problems_with_server = 'Извините, у нас небольшие проблемы с сервером, скоро мы всё починим :)'

    # применение user_agent
    user_agent = UserAgent()
    headers = {
        'User-Agent': user_agent.random
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(DEFAULT_PAGE + word, headers=headers, timeout=3) as response:
                url = str(response.url)
                # проверяем, существует ли перевод введённого слова
                if re.match(r'.*/ooops/.*', url):
                    return error_not_exist_word

                # берём текст из запроса
                html = await response.text()

    except Exception as error:
        print(f'Ha-ha-ha, you caught the error in project "Translator_RU_EN_RU_Bot", in file "parser", in func "get_translation", in request:\n\t{error}')

        with open(f'{PROJECT_PATH}/bot_state.txt', 'a') as bot_state:
            now_time = localtime()

            bot_state.write(error)
            bot_state.write(f' {now_time.tm_hour + TIME_ZONE}.{now_time.tm_min}.{now_time.tm_sec}\n\n')

        return error_problems_with_server

    soup = BeautifulSoup(html, 'html.parser')

    # переводим с русского
    if re.match(r'[а-я]', word):
        try:
            translation_ru = soup.find('p', {'class': 't_inline'}).get_text().strip()
            # добавляем перевод в БД
            asyncio.create_task(
                add_word_translation(database=DATABASE, word=word, from_language=RU, translation=translation_ru)
            )

            # возвращаем полученный перевод
            return translation_ru
        except AttributeError:
            return error_not_exist_word

    # переводим с английского
    else:
        try:
            translation_en = soup.find('div', {'class': 't_inline_en'}).get_text().strip()
            transcription_en = soup.find('div', {'id': 'uk_tr_sound'}).find('span', {'class': 'transcription'}).get_text().strip()

            # добавляем перевод и транскрипцию в БД
            asyncio.create_task(
                add_word_translation(database=DATABASE, word=word, from_language=EN, translation=translation_en, transcription=transcription_en)
            )

            # возвращаем полученный перевод
            return ' '.join((transcription_en, translation_en))
        except AttributeError:
            return error_not_exist_word

# if __name__ == '__main__':
#     word = input('Enter a word: ')
#     word = word.lower()
#
#     tr = get_translation(word)
#     print(tr)
