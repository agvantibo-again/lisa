from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app as app
import click

from datetime import date
import csv
import sys
import shutil
import secrets


class User:
    """Basically a struct representing a user"""

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

    def __repr__(self):
        return f"User {self.name} ({self.real_name}), pw: {self.password_digest}"


def generate_password(dictionary: list, len=3):
    return "-".join([secrets.choice(dictionary) for i in range(len)])


username_prompt = "Internal user name"
cname_prompt = "Frontend user name [visible to them]"
pass_prompt = "New user password"
db_prompt = "Add user to database"


@app.cli.command("mkuser")
@click.option("--name", "-n", prompt=username_prompt, help=username_prompt)
@click.option("--cname", "-c", prompt=cname_prompt, help=cname_prompt)
@click.option("--password", "-p", help=pass_prompt, required=False)
@click.option("--add", is_flag=True, help=pass_prompt)
def create_user(name, cname, password, add):
    if not password:
        dict_file = app.config["PASSWORD_DICT"]
        if not dict_file:
            raise ValueError(
                "No PASSWORD_DICT found. Set LISA_PASSWORD_DICT or add PASSWORD_DICT to configuration"
            )
        with open(app.config["PASSWORD_DICT"]) as pwfile:
            password = generate_password(
                list(map(lambda a: a.strip(), pwfile.readlines()))
            )

    new_user = User(name, cname, dict(), password=password)
    print(new_user)
    print(f"Password: {password}")
    print("To hide the password, run `clear`/`cls`")
    if add or click.confirm("Add user to database?"):
        if new_user.name in app.users.keys():
            if not click.confirm(
                f"User {new_user.name} is already in the database. Overwrite?"
            ):
                return
        app.users[new_user.name] = new_user
        app.data.write()


class Data:
    """An abstraction over the state save/load interface"""

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
