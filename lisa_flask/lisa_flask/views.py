from . import auth
from .user import User

from flask import render_template, request, redirect, url_for
from flask import current_app as app

from datetime import date
import csv


@auth.verify_password
def verify_password(username, password):
    if username in app.users and app.users[username].verify_password(password):
        return username


@app.route("/", methods=["GET"])
@auth.login_required
def get_root():
    user = app.users[auth.current_user()]
    return render_template(
        "index.html",
        user_name=user.real_name,
        app_name="LISA",
        date_now=date.today().isoformat(),
        data=reversed(app.users[auth.current_user()].data.items()),
    )


@app.route("/submit", methods=["POST"])
@auth.login_required
def post_submit():
    user = app.users[auth.current_user()]
    data = request.form
    user.data[date.today().isoformat()] = data["hours"]
    app.data.write()

    return redirect(url_for("get_root"))
