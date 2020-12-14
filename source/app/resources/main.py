from flask import redirect, url_for, render_template
from flask_login import current_user

from app.helpers.login import authenticated


def index():
    if authenticated() == True:
        if current_user.roles.first().name == "Administrador":
            return redirect(url_for("user_index"))
        return redirect(url_for("user_index"))
    else:
        return redirect(url_for("auth_login"))
