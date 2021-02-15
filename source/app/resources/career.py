
from flask import redirect, render_template, request, url_for
from flask_login import current_user

from app.models.configuration import Configuration
from app.models.alert import Alert
from app.helpers.alert import add_alert, get_alert
from app.helpers.permission import permission
from app.models import Career
from app.helpers.forms import CareerForm, CareerReport


@permission('career_index')
def index():
    allowed_career_ids = None

    if not current_user.is_admin():
        allowed_career_ids = current_user.allowed_career_id_list()

    careers = Career.all_paginated(page=int(request.args.get('page', 1)),
                                   per_page=Configuration.get().items_per_page, ids=allowed_career_ids)
    return render_template("career/index.html", careers=careers, alert=get_alert())


@permission('career_show')
def show(id):
    career = Career.get(id)
    if not career:
        add_alert(Alert("danger", "La carrera no existe."))
        return redirect(url_for("career_index"))

    return render_template("career/show.html", career=career)


@permission('career_create')
def new():
    return render_template("career/new.html", form=CareerForm())


@permission('career_create')
def create():
    form = CareerForm(id=None)
    if form.validate_on_submit():
        career = Career(name=form.name.data)
        career.save()
        add_alert(
            Alert("success", f'La carrera "{career.name}" se ha creado correctamente.'))
        return redirect(url_for("career_index"))
    return render_template("career/new.html", form=form)


@permission('career_update')
def edit(id):
    career = Career.get(id)
    if not career:
        add_alert(Alert("danger", "La carrera no existe."))
        return redirect(url_for("career_index"))

    form = CareerForm(obj=career)

    return render_template("career/edit.html", career=career, form=form)


@permission('career_update')
def update(id):
    career = Career.get(id)
    if not career:
        add_alert(Alert("danger", "La carrera no existe."))
        return redirect(url_for("career_index"))
    form = CareerForm(id=id)
    if not form.validate_on_submit():
        return render_template("career/edit.html", career=career, form=form)
    career.update(name=form.name.data)
    add_alert(
        Alert("success", f'La carrera "{career.name}" se ha modificado correctamente.'))
    return redirect(url_for("career_index"))


@permission('career_delete')
def delete(id):
    career = Career.get(id)
    if not career or career.is_deleted:
        add_alert(Alert("danger", "La carrera no existe."))
    elif career.has_cathedras():
        add_alert(Alert("danger", "La carrera no debe poseer catedras"))
    elif career.has_users():
        add_alert(Alert("danger", "La carrera no debe poseer responsables"))
    else:
        career.remove()
        add_alert(
            Alert("success", f'La carrera "{career.name}" se ha borrado correctamente.'))
    return redirect(url_for("career_index"))


@permission('career_report')
def report():

    form = CareerReport(request.args)
    args = {
        "careers": form.careers.data,
        "employee_type": form.employee_type.data,
        "charges_ids": form.charges.data,
        "institutional_email": form.institutional_email.data if form.institutional_email.data != "" else None,
        "name": form.name.data if form.name.data != "" else None,
        "surname": form.surname.data if form.surname.data != "" else None,
        "secondary_email": form.secondary_email.data if form.secondary_email.data != "" else None,
        "dni": form.dni.data if form.dni.data != "" else None
    }

    careers = []
    if current_user.is_admin() or current_user.is_visitante():
        careers = Career.all()
    else:
        careers = [current_user.get_career()]

    form.careers.choices = careers.collect(
        lambda each: (each.id, each.name))

    careers_staff = []
    json_export = {}
    export = {}
    if request.args:
        data = Career.search(
            form.show_dni.data, form.show_secondary_email.data, **args)
        careers_staff = data["career_list"]
        export = data["export"]
        # Obsoleto
        json_export = data["staff_json"]

    return render_template("career/report.html", export=export, careers=careers_staff, dni_field=form.show_dni.data, secondary_email_field=form.show_secondary_email.data, form=form)
