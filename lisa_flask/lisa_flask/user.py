from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app as app

from datetime import date
import csv


class User:
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

    def serialize(self, ostream):
        swriter = csv.writer(ostream, dialect="excel")
        swriter.writerow(name, real_name, data, password_digest)
