
from flask import redirect, render_template, request, url_for
from flask_login import current_user

from app.models.configuration import Configuration
from app.models.alert import Alert
from app.helpers.alert import add_alert, get_alert
from app.helpers.permission import permission
from app.models import Office
from app.helpers.forms import OfficeForm

@permission('office_index')
def index():
    allowed_office_ids = None

    if not current_user.is_admin():
        allowed_office_ids = current_user.allowed_office_id_list()

    offices = Office.all_paginated(page=int(request.args.get('page', 1)),
                        per_page=Configuration.get().items_per_page, ids=allowed_office_ids)
    return render_template("office/index.html", offices=offices, alert=get_alert())


@permission('office_show')
def show(id):
    office = Office.get(id)
    if not office:
        add_alert(Alert("danger", "El oficina no existe."))
        return redirect(url_for("office_index"))

    return render_template("office/show.html", office=office)

@permission('office_create')
def new():
    return render_template("office/new.html", form=OfficeForm())

@permission('office_create')
def create():
    form = OfficeForm(id=None)
    if form.validate_on_submit():
        office = Office(name = form.name.data, email = form.email.data, phone = form.phone.data, location = form.location.data)
        office.save()
        add_alert(
            Alert("success", f"El {office.name} se a creado correctamente."))
        return redirect(url_for("office_index"))
    return render_template("office/new.html", form=form)

@permission('office_update')
def edit(id):
    office = Office.get(id)
    if not office:
        add_alert(Alert("danger", "El oficina no existe."))
        return redirect(url_for("office_index"))

    form = OfficeForm(obj=office)

    return render_template("office/edit.html", office=office, form=form)

@permission('office_update')
def update(id):
    office = Office.get(id)
    if not office:
        add_alert(Alert("danger", "El oficina no existe."))
        return redirect(url_for("office_index"))
    form = OfficeForm(id=id)
    if not form.validate_on_submit():
        return render_template("office/edit.html", office=office, form=form)
    office.update(name = form.name.data, email = form.email.data, phone = form.phone.data, location = form.location.data)
    add_alert(
        Alert("success", f"El {office.name} se a modificado correctamente."))
    return redirect(url_for("office_index"))

@permission('office_delete')
def delete(id):
    office = Office.get(id)
    if not office or office.is_deleted:
        add_alert(Alert("danger", "El oficina no existe."))
    else:
        office.remove()
        add_alert(
                Alert("success", f"El {office.name} se a borrado correctamente."))
    return redirect(url_for("office_index"))