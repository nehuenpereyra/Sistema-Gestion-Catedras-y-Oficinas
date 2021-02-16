from flask import redirect, render_template, url_for
from flask_login import login_user, logout_user
from flask_login import current_user

from app.models import User
from app.helpers.forms.login_form import LoginForm
from app.helpers.login import authenticated
from app.models.alert import Alert
from app.helpers.alert import get_alert, add_alert


def login():
    if authenticated() == True:
        return redirect(url_for("index"))
    return render_template("auth/login.html", alert=get_alert(), form=LoginForm())


def authenticate():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.login(form.username.data, form.password.data)
        if user:
            if not user.is_responsible() or user.is_responsible_of_elements():
                login_user(user, remember=form.remember_me.data)
                user.remove_recovery_link()
                return redirect(url_for("index"))
            if user.is_career_manager():
                add_alert(Alert(
                    "danger", f'No posee carreras asignadas.'))
            if user.is_cathedra_manager():
                add_alert(Alert(
                    "danger", f'No posee cátedras asignadas.'))
            if user.is_office_manager():
                add_alert(Alert(
                    "danger", f'No posee oficinas asignadas.'))
        else:
            add_alert(Alert(
                "danger", f'Usuario o clave incorrecto.'))
    return render_template("auth/login.html", form=form, alert=get_alert(), authError=True)


def logout():
    logout_user()
    return redirect(url_for("index"))
