from os.path import abspath


# путь до папки с проектом "Translator_RU_EN_RU_Bot"
path_list = abspath('constants.py').split('/')
PROJECT_PATH = '/'.join(path_list[:path_list.index('Translator_RU_EN_RU_Bot') + 1])
# print(PROJECT_PATH)

DATABASE = f'{PROJECT_PATH}/sqlite.db'

# для локалки
TIME_ZONE = 0
# для сервака
# TIME_ZONE = 3

DEFAULT_PAGE = 'https://wooordhunt.ru/word/'
RU = 'russian'
EN = 'english'
