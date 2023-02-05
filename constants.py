import sqlite3


DATABASE = './sqlite.db'
CONNECTION = sqlite3.connect(DATABASE)
DEFAULT_PAGE = 'https://wooordhunt.ru/word/'
RU = 'russian'
EN = 'english'
