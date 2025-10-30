from flask import Flask, g
from flask_httpauth import HTTPBasicAuth
from .user import User
import csv
import logging
import os


def mk_app():
    app = Flask(__name__)

    with app.app_context():
        from lisa_flask import views

    app.config["DATA_DIR"] = (
        os.environ["LISA_DATA_DIR"]
        if "LISA_DATA_DIR" in os.environ.keys()
        else "./data"
    )

    with app.app_context():
        app.users = {
            "agvantibo": User("agvantibo", "Разработчик Битович", dict(), password="admin")
        }  # TODO: implement actual user loading

        try:
            with open(os.path.join(app.config["DATA_DIR"], "config.yml")) as confile:
                data = load(confile, loader=Loader)
            app.config.update(data)
        except FileNotFoundError as err:
            print(f"Unable to load config: {err}")

        app.logger.setLevel(
            logging.INFO
        )  # TODO: implement switching logic based on configuration
   
    return app

auth = HTTPBasicAuth()

from yaml import load, dump

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper
