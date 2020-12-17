from os import sys
from flask import redirect, render_template, request, url_for
from flask_login import current_user

from app.models.configuration import Configuration
from app.models.alert import Alert
from app.helpers.alert import add_alert, get_alert
from app.helpers.permission import permission
from app.models import Request, User, RequestType, MailSender
from app.helpers.forms import RequestForm
from datetime import datetime

@permission('request_index')
def index():
    allowed_request_ids = None

    if not current_user.is_admin():
        allowed_request_ids = current_user.allowed_request_id_list()

    requests = Request.all_paginated(page=int(request.args.get('page', 1)),
                        per_page=Configuration.get().items_per_page, ids=allowed_request_ids)

    if not current_user.is_admin():
        request_types = RequestType.find_by_state(True)
        query_tecnical = RequestType.all().detect(lambda each: each.name == "Consulta Tecnica")
        request_types.remove(query_tecnical)
        requests = {}
        for request_type in request_types:
            requests[str(request_type.id)] = Request.reverse_all().select(lambda each: each.request_type_id == request_type.id)
        return render_template("request/index.html", requests=requests, request_types=request_types, form=RequestForm(), alert=get_alert())
    
    return render_template("request/authorized_index.html", requests=requests, alert=get_alert())


@permission('request_show')
def show(id):
    request = Request.get(id)
    if not request:
        add_alert(Alert("danger", "El solicitud no existe."))
        return redirect(url_for("request_index"))

    return render_template("request/show.html", request=request)

@permission('request_create')
def support():
    return render_template("request/new.html", alert=get_alert(), form=RequestForm())

@permission('request_create')
def create():
    form = RequestForm(id=None)
    if form.validate_on_submit():
        is_technical = False
        request_type_id = request.args.get("request_type")
        if not request_type_id:
            is_technical = True
            request_type_id = RequestType.all().detect(lambda each: each.name == "Consulta Tecnica").id
        try:
            MailSender.send(f"Nueva solicitud de: {RequestType.get(request_type_id).name}", form.content.data)
        except:
            add_alert(
                    Alert("danger", f'Ha fallado al intentar enviar el correo.'))
            if is_technical:
                return redirect(url_for("request_support"))
            return redirect(url_for("request_index"))
        new_request = Request(content = form.content.data, is_resolved = False, receive_email = form.receive_email.data, timestamp = datetime.today(), user = User.get(current_user.id), request_type = RequestType.get(request_type_id))
        new_request.save()
        if is_technical:
            add_alert(
                Alert("success", f'La consulta se ha enviado correctamente.'))
            return redirect(url_for("request_support"))
        add_alert(
            Alert("success", f'La solicitud se ha creado correctamente.'))
        return redirect(url_for("request_index"))
    return render_template("request/new.html", form=form)

@permission('request_update')
def edit(id):
    request = Request.get(id)
    if not request:
        add_alert(Alert("danger", "El solicitud no existe."))
        return redirect(url_for("request_index"))

    form = RequestForm(obj=request)
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
        Alert("success", f'El solicitud "{request.content}" se ha modificado correctamente.'))
    return redirect(url_for("request_index"))

@permission('request_delete')
def solved(id):
    request_ = Request.get(id)
    if not request_ or request_.is_deleted:
        add_alert(Alert("danger", "El solicitud no existe."))
    else:
        if request_.receive_email == True:
            try:
                MailSender.send_to_user(f"Se resolvio tu solicitud de {request_.request_type.name}", "Se te escribira a la brevedad...", request_.user.institutional_email)
            except:
                add_alert(
                        Alert("danger", f'Ha fallado el envio de correo.'))
                return redirect(url_for("request_index"))
        request_.is_resolved = True
        request_.save()
        add_alert(
                Alert("success", f'La solicitud de "{request_.user.name}" se ha resuelto correctamente.'))
    return redirect(url_for("request_index"))