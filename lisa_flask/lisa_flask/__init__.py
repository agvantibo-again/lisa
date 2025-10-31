from flask import Flask, g
from flask_httpauth import HTTPBasicAuth
from .user import User
import csv
import yaml
import logging
import os

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper
# pyyaml import boilerplate to load native libraries


def mk_app():
    app = Flask(__name__)

    with app.app_context():
        from lisa_flask import views

    app.config["DATA_DIR"] = (
        os.environ["LISA_DATA_DIR"]
        if "LISA_DATA_DIR" in os.environ.keys()
        else "./data"
    )
    app.config["LOG_LEVEL"] = 6
    app.config["TESTING"] = False
    app.config["CSV_DIALECT"] = "excel"
    config_path = os.path.join(app.config["DATA_DIR"], "config.yml")

    with app.app_context():
        try:
            with open(config_path) as confile:
                conf = yaml.load(confile, Loader=Loader)
            app.config.update(conf)
        except FileNotFoundError as err:
            app.logger.error(f"Unable to load config: {err}")

        app.logger.setLevel(int(app.config["LOG_LEVEL"]))

        if "DATA_FILE" not in app.config.keys():
            raise ValueError(
                f"DATA_FILE not set in configuration {config_path}, cannot continue!"
            )

        data_path = os.path.join(app.config["DATA_DIR"], app.config["DATA_FILE"])
        app.users = dict()
        with open(data_path) as datafile:
            data = csv.reader(datafile, dialect="excel")
            table_headers = next(data)[3:]
            for username, realname, pwdigest, *user_data in data:
                user_ddict = dict()
                for i_cell in range(len(user_data)):
                    if user_data[i_cell]:
                        user_ddict[table_headers[i_cell]] = int(user_data[i_cell])
                app.users[username] = User(
                    username, realname, user_ddict, new_password_digest=pwdigest
                )

    return app


auth = HTTPBasicAuth()
