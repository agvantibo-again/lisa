from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app as app

from datetime import date
import csv
import shutil


class User:
    '''Basically a struct representing a user'''
    name: str = "nobody"
    real_name: str = "Критическая Ошибка"
    data: dict = {}
    password_digest: str = ""

    def __init__(
        self, new_name, new_real_name, new_data, new_password_digest="", password=""
    ):
        self.name = new_name
        self.real_name = new_real_name
        self.data = new_data
        if password:
            self.password_digest = generate_password_hash(password)
            app.logger.warning(f"Passing cleartext password to user {new_name}")
        elif new_password_digest:
            self.password_digest = new_password_digest

    def verify_password(self, new_password):
        return check_password_hash(self.password_digest, new_password)


class Data:
    '''An abstraction over the state save/load interface'''
    store = dict()
    path = ""
    dialect = "excel"
    table_h0 = ("Имя пользователя", "Кириллическое имя", "Хеш пароля")
    def __init__(self, data_path, dialect="excel", **kwargs):
        self.path = data_path
        with open(data_path) as datafile:
            self.dialect = dialect
            data = csv.reader(datafile, dialect=self.dialect)

            table_headers = next(data)[3:]
            for username, realname, pwdigest, *user_data in data:
                user_ddict = dict()
                for i_cell in range(len(user_data)):
                    if user_data[i_cell]:
                        user_ddict[table_headers[i_cell]] = int(user_data[i_cell])
                self.store[username] = User(
                    username, realname, user_ddict, new_password_digest=pwdigest
                )

    def write(self):
        table_headers = list(self.table_h0)
        dates = set()
        for user in self.store.values():
            dates.update(user.data.keys())
        dates = list(sorted(dates))
        table_headers += dates
        with open(self.path + ".new", "w") as new_file:
            new_writer = csv.writer(new_file, dialect=self.dialect)
            new_writer.writerow(table_headers)
            for user in self.store.values():
                user_line = [user.name, user.real_name, user.password_digest]
                for date in dates:
                    user_line.append(user.data.get(date, "0"))
                new_writer.writerow(user_line)

        shutil.move(self.path, self.path + ".bak")
        shutil.move(self.path + ".new", self.path)
