
from flask import redirect, render_template, request, url_for
from flask_login import current_user

from app.models.configuration import Configuration
from app.models.alert import Alert
from app.helpers.alert import add_alert, get_alert
from app.helpers.permission import permission
from app.models import Role, Permission
from app.helpers.forms import RoleForm

@permission('role_index')
def index():
    allowed_role_ids = None

    if not current_user.is_admin():
        allowed_role_ids = current_user.allowed_role_id_list()

    roles = Role.all_paginated(page=int(request.args.get('page', 1)),
                        per_page=Configuration.get().items_per_page, ids=allowed_role_ids)
    return render_template("role/index.html", roles=roles, alert=get_alert())


@permission('role_show')
def show(id):
    role = Role.get(id)
    if not role:
        add_alert(Alert("danger", "El rol no existe."))
        return redirect(url_for("role_index"))

    return render_template("role/show.html", role=role)

@permission('role_create')
def new():
    return render_template("role/new.html", form=RoleForm())

@permission('role_create')
def create():
    form = RoleForm(id=None)
    if form.validate_on_submit():
        role = Role(name = form.name.data, permissions = Permission.get_all(form.permissions.data))
        role.save()
        add_alert(
            Alert("success", f'El rol "{role.name}" se ha creado correctamente.'))
        return redirect(url_for("role_index"))
    return render_template("role/new.html", form=form)

@permission('role_update')
def edit(id):
    role = Role.get(id)
    if not role:
        add_alert(Alert("danger", "El rol no existe."))
        return redirect(url_for("role_index"))

    form = RoleForm(obj=role)
    if role.permissions is not None:
        form.permissions.data = role.permissions.collect(lambda each: each.id)    

    return render_template("role/edit.html", role=role, form=form)

@permission('role_update')
def update(id):
    role = Role.get(id)
    if not role:
        add_alert(Alert("danger", "El rol no existe."))
        return redirect(url_for("role_index"))
    form = RoleForm(id=id)
    if not form.validate_on_submit():
        return render_template("role/edit.html", role=role, form=form)
    role.update(name = form.name.data, permissions = Permission.get_all(form.permissions.data))
    add_alert(
        Alert("success", f'El rol "{role.name}" se ha modificado correctamente.'))
    return redirect(url_for("role_index"))

@permission('role_delete')
def delete(id):
    role = Role.get(id)
    if not role or role.is_deleted:
        add_alert(Alert("danger", "El rol no existe."))
    else:
        role.remove()
        add_alert(
                Alert("success", f'El rol "{role.name}" se ha borrado correctamente.'))
    return redirect(url_for("role_index"))