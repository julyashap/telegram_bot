from configparser import ConfigParser
import os

# подключение к токену бота через модуль os (токен в переменных среды)
TOKEN_FOR_DANCE_BOT = os.getenv('TOKEN_FOR_DANCE_BOT')


# инофрмация для БД
def config(filename="database.ini", section="postgresql"):
    parser = ConfigParser()

    parser.read(filename)
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception(
            'Section {0} is not found in the {1} file.'.format(section, filename))
    return db
