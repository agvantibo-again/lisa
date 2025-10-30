import random
import os
import sys
from .user import User


dpath = os.path.join(app.config["DATA_DIR"], "dictionary.txt")


def generate():
    new_name = input("Внутреннее имя пользователя (lat) >> ")
    new_real_name = input("Кириллическое имя пользователя [видно ему] >> ")
    new_password = input("Пароль >> ")

    user = User(new_name, new_real_name, dict(), password="")
    user.serialize(sys.stdout)


if __name__ == "__main__":
    generate()
