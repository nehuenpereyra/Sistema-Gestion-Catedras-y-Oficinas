from flask import redirect, render_template, url_for
from flask_login import login_user, logout_user
from flask_login import current_user

from app.models import User
from app.helpers.forms.login_form import LoginForm
from app.helpers.login import authenticated


def login():
    if authenticated() == True:
        return redirect(url_for("index"))
    return render_template("auth/login.html", form=LoginForm())


def authenticate():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.login(form.username.data, form.password.data)
        if user:
            login_user(user, remember=form.remember_me.data)
            return redirect(url_for("index"))
    return render_template("auth/login.html", form=form, authError=True)


def logout():
    logout_user()
    return redirect(url_for("index"))
