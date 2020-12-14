
from flask import redirect, render_template, request, url_for
from flask_login import current_user

from app.models.configuration import Configuration
from app.models.alert import Alert
from app.helpers.alert import add_alert, get_alert
from app.helpers.permission import permission
from app.models import Permission, Role
from app.helpers.forms import PermissionForm

@permission('permission_index')
def index():
    allowed_permission_ids = None

    if not current_user.is_admin():
        allowed_permission_ids = current_user.allowed_permission_id_list()

    permissions = Permission.all_paginated(page=int(request.args.get('page', 1)),
                        per_page=Configuration.get().items_per_page, ids=allowed_permission_ids)
    return render_template("permission/index.html", permissions=permissions, alert=get_alert())


@permission('permission_show')
def show(id):
    permission = Permission.get(id)
    if not permission:
        add_alert(Alert("danger", "El permiso no existe."))
        return redirect(url_for("permission_index"))

    return render_template("permission/show.html", permission=permission)

@permission('permission_create')
def new():
    return render_template("permission/new.html", form=PermissionForm())

@permission('permission_create')
def create():
    form = PermissionForm(id=None)
    if form.validate_on_submit():
        permission = Permission(name = form.name.data, roles = Role.get_all(form.roles.data))
        permission.save()
        add_alert(
            Alert("success", f"El {permission.name} se a creado correctamente."))
        return redirect(url_for("permission_index"))
    return render_template("permission/new.html", form=form)

@permission('permission_update')
def edit(id):
    permission = Permission.get(id)
    if not permission:
        add_alert(Alert("danger", "El permiso no existe."))
        return redirect(url_for("permission_index"))

    form = PermissionForm(obj=permission)
    if permission.roles is not None:
        form.roles.data = permission.roles.collect(lambda each: each.id)    

    return render_template("permission/edit.html", permission=permission, form=form)

@permission('permission_update')
def update(id):
    permission = Permission.get(id)
    if not permission:
        add_alert(Alert("danger", "El permiso no existe."))
        return redirect(url_for("permission_index"))
    form = PermissionForm(id=id)
    if not form.validate_on_submit():
        return render_template("permission/edit.html", permission=permission, form=form)
    permission.update(name = form.name.data, roles = Role.get_all(form.roles.data))
    add_alert(
        Alert("success", f"El {permission.name} se a modificado correctamente."))
    return redirect(url_for("permission_index"))

@permission('permission_delete')
def delete(id):
    permission = Permission.get(id)
    if not permission or permission.is_deleted:
        add_alert(Alert("danger", "El permiso no existe."))
    else:
        permission.remove()
        add_alert(
                Alert("success", f"El {permission.name} se a borrado correctamente."))
    return redirect(url_for("permission_index"))