
from flask import redirect, render_template, request, url_for
from flask_login import current_user

from app.models.configuration import Configuration
from app.models.alert import Alert
from app.helpers.alert import add_alert, get_alert
from app.helpers.permission import permission
from app.models import Request, User, RequestType
from app.helpers.forms import RequestForm

@permission('request_index')
def index():
    allowed_request_ids = None

    if not current_user.is_admin():
        allowed_request_ids = current_user.allowed_request_id_list()

    requests = Request.all_paginated(page=int(request.args.get('page', 1)),
                        per_page=Configuration.get().items_per_page, ids=allowed_request_ids)
    return render_template("request/index.html", requests=requests, alert=get_alert())


@permission('request_show')
def show(id):
    request = Request.get(id)
    if not request:
        add_alert(Alert("danger", "El solicitud no existe."))
        return redirect(url_for("request_index"))

    return render_template("request/show.html", request=request)

@permission('request_create')
def new():
    return render_template("request/new.html", form=RequestForm())

@permission('request_create')
def create():
    form = RequestForm(id=None)
    if form.validate_on_submit():
        request = Request(content = form.content.data, is_resolved = form.is_resolved.data, receive_email = form.receive_email.data, timestamp = form.timestamp.data, user = User.get(form.user.data), request_type = RequestType.get(form.request_type.data))
        request.save()
        add_alert(
            Alert("success", f"El {request.content} se a creado correctamente."))
        return redirect(url_for("request_index"))
    return render_template("request/new.html", form=form)

@permission('request_update')
def edit(id):
    request = Request.get(id)
    if not request:
        add_alert(Alert("danger", "El solicitud no existe."))
        return redirect(url_for("request_index"))

    form = RequestForm(obj=request)
    form.user.data = request.user.id    
    form.request_type.data = request.request_type.id    

    return render_template("request/edit.html", request=request, form=form)

@permission('request_update')
def update(id):
    request = Request.get(id)
    if not request:
        add_alert(Alert("danger", "El solicitud no existe."))
        return redirect(url_for("request_index"))
    form = RequestForm(id=id)
    if not form.validate_on_submit():
        return render_template("request/edit.html", request=request, form=form)
    request.update(content = form.content.data, is_resolved = form.is_resolved.data, receive_email = form.receive_email.data, timestamp = form.timestamp.data, user = User.get(form.user.data), request_type = RequestType.get(form.request_type.data))
    add_alert(
        Alert("success", f"El {request.content} se a modificado correctamente."))
    return redirect(url_for("request_index"))

@permission('request_delete')
def delete(id):
    request = Request.get(id)
    if not request or request.is_deleted:
        add_alert(Alert("danger", "El solicitud no existe."))
    else:
        request.remove()
        add_alert(
                Alert("success", f"El {request.content} se a borrado correctamente."))
    return redirect(url_for("request_index"))