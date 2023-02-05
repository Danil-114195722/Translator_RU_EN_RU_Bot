import sqlite3


# для локалки
# DATABASE = '/home/daniil/Documents/Python/Telegram_bots/Translator_RU_EN_RU_Bot/sqlite.db'
# для сервака
DATABASE = './sqlite.db'
CONNECTION = sqlite3.connect(DATABASE)
DEFAULT_PAGE = 'https://wooordhunt.ru/word/'
RU = 'russian'
EN = 'english'
