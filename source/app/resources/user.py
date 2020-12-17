
from flask import redirect, render_template, request, url_for
from flask_login import current_user

from app.models.configuration import Configuration
from app.models.alert import Alert
from app.helpers.alert import add_alert, get_alert
from app.helpers.permission import permission
from app.models import User, Role
from app.helpers.forms import UserForm


@permission('user_index')
def index():
    allowed_user_ids = None

    if not current_user.is_admin():
        allowed_user_ids = current_user.allowed_user_id_list()

    users = User.all_paginated(page=int(request.args.get('page', 1)),
                               per_page=Configuration.get().items_per_page, ids=allowed_user_ids)
    return render_template("user/index.html", users=users, alert=get_alert())


@permission('user_show')
def show(id):
    user = User.get(id)
    if not user:
        add_alert(Alert("danger", "El usuario no existe."))
        return redirect(url_for("user_index"))

    return render_template("user/show.html", user=user)


@permission('user_create')
def new():
    return render_template("user/new.html", form=UserForm())


@permission('user_create')
def create():
    form = UserForm(id=None)
    if form.validate_on_submit():
        user = User(name=form.name.data, surname=form.surname.data, username=form.username.data,
                    institutional_email=form.institutional_email.data, secondary_email=form.secondary_email.data)
        user.set_password(form.password.data)
        user.set_roles(Role.get_all(form.roles.data))
        user.save()
        add_alert(
            Alert("success", f'El usuario "{user.name}" se ha creado correctamente.'))
        return redirect(url_for("user_index"))
    return render_template("user/new.html", form=form)


@permission('user_update')
def edit(id):
    user = User.get(id)
    if not user:
        add_alert(Alert("danger", "El usuario no existe."))
        return redirect(url_for("user_index"))

    form = UserForm(obj=user)
    form.roles.data = user.roles.collect(lambda each: each.id)

    return render_template("user/edit.html", user=user, form=form)


@permission('user_update')
def update(id):
    user = User.get(id)
    if not user:
        add_alert(Alert("danger", "El usuario no existe."))
        return redirect(url_for("user_index"))
    form = UserForm(id=id)
    if not form.validate_on_submit():
        return render_template("user/edit.html", user=user, form=form)
    user.set_password(form.password.data)
    user.update(name=form.name.data, surname=form.surname.data, username=form.username.data, password=form.password.data,
                institutional_email=form.institutional_email.data, secondary_email=form.secondary_email.data, roles=Role.get_all(form.roles.data))
    add_alert(
        Alert("success", f'El usuario "{user.name}" se ha modificado correctamente.'))
    return redirect(url_for("user_index"))


@permission('user_delete')
def delete(id):
    user = User.get(id)
    if not user or user.is_deleted:
        add_alert(Alert("danger", "El usuario no existe."))
    else:
        user.remove()
        add_alert(
            Alert("success", f'El usuario "{user.name}" se ha borrado correctamente.'))
    return redirect(url_for("user_index"))
