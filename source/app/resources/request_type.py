
from flask import redirect, render_template, request, url_for
from flask_login import current_user

from app.models.configuration import Configuration
from app.models.alert import Alert
from app.helpers.alert import add_alert, get_alert
from app.helpers.permission import permission
from app.models import RequestType
from app.helpers.forms import RequestTypeForm

@permission('request_type_index')
def index():
    allowed_request_type_ids = None

    if not current_user.is_admin():
        allowed_request_type_ids = current_user.allowed_request_type_id_list()

    request_types = RequestType.all_paginated(page=int(request.args.get('page', 1)),
                        per_page=Configuration.get().items_per_page, ids=allowed_request_type_ids)
    return render_template("request_type/index.html", request_types=request_types, alert=get_alert())


@permission('request_type_show')
def show(id):
    request_type = RequestType.get(id)
    if not request_type:
        add_alert(Alert("danger", "El tipo de solicitud no existe."))
        return redirect(url_for("request_type_index"))

    return render_template("request_type/show.html", request_type=request_type)

@permission('request_type_create')
def new():
    return render_template("request_type/new.html", form=RequestTypeForm())

@permission('request_type_create')
def create():
    form = RequestTypeForm(id=None)
    if form.validate_on_submit():
        request_type = RequestType(name = form.name.data, message = form.message.data, state = form.state.data)
        request_type.save()
        add_alert(
            Alert("success", f'El tipo de solicitud "{request_type.name}" se ha creado correctamente.'))
        return redirect(url_for("request_type_index"))
    return render_template("request_type/new.html", form=form)

@permission('request_type_update')
def edit(id):
    request_type = RequestType.get(id)
    if not request_type:
        add_alert(Alert("danger", "El tipo de solicitud no existe."))
        return redirect(url_for("request_type_index"))

    form = RequestTypeForm(obj=request_type)

    return render_template("request_type/edit.html", request_type=request_type, form=form)

@permission('request_type_update')
def update(id):
    request_type = RequestType.get(id)
    if not request_type:
        add_alert(Alert("danger", "El tipo de solicitud no existe."))
        return redirect(url_for("request_type_index"))
    form = RequestTypeForm(id=id)
    if not form.validate_on_submit():
        return render_template("request_type/edit.html", request_type=request_type, form=form)
    request_type.update(name = form.name.data, message = form.message.data, state = form.state.data)
    add_alert(
        Alert("success", f'El tipo de solicitud "{request_type.name}" se ha modificado correctamente.'))
    return redirect(url_for("request_type_index"))

@permission('request_type_delete')
def delete(id):
    request_type = RequestType.get(id)
    if not request_type or request_type.is_deleted:
        add_alert(Alert("danger", "El tipo de solicitud no existe."))
    else:
        request_type.remove()
        add_alert(
                Alert("success", f'El tipo de solicitud "{request_type.name}" se ha borrado correctamente.'))
    return redirect(url_for("request_type_index"))