from flask import redirect, url_for, render_template
from flask_login import current_user

from app.helpers.login import authenticated


def index():
    if authenticated() == True:
        if current_user.is_admin():
            return redirect(url_for("user_index"))
        if current_user.is_cathedra_manager():
            return redirect(url_for("cathedra_index"))
        if current_user.is_career_manager():
            return redirect(url_for("career_index"))
        if current_user.is_office_manager():
            return redirect(url_for("office_index"))
        return redirect(url_for("cathedra_report"))
    else:
        return redirect(url_for("auth_login"))
