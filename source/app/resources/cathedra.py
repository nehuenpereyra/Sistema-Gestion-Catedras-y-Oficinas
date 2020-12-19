import json
from flask import redirect, render_template, request, url_for, make_response
from flask_login import current_user

from app.models.configuration import Configuration
from app.models.alert import Alert
from app.helpers.alert import add_alert, get_alert
from app.helpers.permission import permission
from app.models import Cathedra, Career
from app.helpers.forms import CathedraForm, CathedraReport


@permission('cathedra_index')
def index():
    allowed_cathedra_ids = None

    if not current_user.is_admin():
        allowed_cathedra_ids = current_user.allowed_cathedra_id_list()

    cathedras = Cathedra.all_paginated(page=int(request.args.get('page', 1)),
                                       per_page=Configuration.get().items_per_page, ids=allowed_cathedra_ids)
    return render_template("cathedra/index.html", cathedras=cathedras, alert=get_alert())


@permission('cathedra_show')
def show(id):
    cathedra = Cathedra.get(id)
    if not cathedra:
        add_alert(Alert("danger", "El cátedra no existe."))
        return redirect(url_for("cathedra_index"))

    return render_template("cathedra/show.html", cathedra=cathedra)


@permission('cathedra_create')
def new():
    return render_template("cathedra/new.html", form=CathedraForm())


@permission('cathedra_create')
def create():
    form = CathedraForm(id=None)
    if form.validate_on_submit():
        cathedra = Cathedra(name=form.name.data, email=form.email.data, phone=form.phone.data,
                            location=form.location.data, attention_time=form.attention_time.data, career=Career.get(form.career.data))
        cathedra.save()
        add_alert(
            Alert("success", f'El cátedra "{cathedra.name}" se ha creado correctamente.'))
        return redirect(url_for("cathedra_index"))
    return render_template("cathedra/new.html", form=form)


@permission('cathedra_update')
def edit(id):
    cathedra = Cathedra.get(id)
    if not cathedra:
        add_alert(Alert("danger", "El cátedra no existe."))
        return redirect(url_for("cathedra_index"))

    form = CathedraForm(obj=cathedra)
    form.career.data = cathedra.career.id

    return render_template("cathedra/edit.html", cathedra=cathedra, form=form)


@permission('cathedra_update')
def update(id):
    cathedra = Cathedra.get(id)
    if not cathedra:
        add_alert(Alert("danger", "El cátedra no existe."))
        return redirect(url_for("cathedra_index"))
    form = CathedraForm(id=id)
    if not form.validate_on_submit():
        return render_template("cathedra/edit.html", cathedra=cathedra, form=form)
    cathedra.update(name=form.name.data, email=form.email.data, phone=form.phone.data, location=form.location.data,
                    attention_time=form.attention_time.data, career=Career.get(form.career.data))
    add_alert(
        Alert("success", f'El cátedra "{cathedra.name}" se ha modificado correctamente.'))
    return redirect(url_for("cathedra_index"))


@permission('cathedra_delete')
def delete(id):
    cathedra = Cathedra.get(id)
    if not cathedra or cathedra.is_deleted:
        add_alert(Alert("danger", "El cátedra no existe."))
    else:
        cathedra.remove()
        add_alert(
            Alert("success", f'El cátedra "{cathedra.name}" se ha borrado correctamente.'))
    return redirect(url_for("cathedra_index"))


def report():

    form = CathedraReport(request.args)
    args = {
        "cathedras": form.cathedras.data,
        "employee_type": form.employee_type.data,
        "charges_ids": form.charges.data,
        "institutional_email": form.institutional_email.data if form.institutional_email.data != "" else None,
        "name": form.name.data if form.name.data != "" else None,
        "surname": form.surname.data if form.surname.data != "" else None,
        "secondary_email": form.secondary_email.data if form.secondary_email.data != "" else None,
        "dni": form.dni.data if form.dni.data != "" else None
    }

    cathedras = []
    if current_user.is_admin() or current_user.is_visitante():
        cathedras = Cathedra.all()
    else:
        cathedras = current_user.get_cathedras()
    form.cathedras.choices = cathedras.collect(
        lambda each: (each.id, each.name))

    cathedras_staff = []
    json_export = {}
    if request.args:
        data = Cathedra.search(
            form.show_dni.data, form.show_secondary_email.data, **args)
        cathedras_staff = data["cathedra_list"]
        json_export = data["staff_json"]

    return render_template("cathedra/report.html", json_export=json_export, cathedras=cathedras_staff, dni_field=form.show_dni.data, secondary_email_field=form.show_secondary_email.data, form=form)
