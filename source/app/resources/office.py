
from flask import redirect, render_template, request, url_for
from flask_login import current_user

from app.models.configuration import Configuration
from app.models.alert import Alert
from app.helpers.alert import add_alert, get_alert
from app.helpers.permission import permission
from app.models import Office, Charge
from app.helpers.forms import OfficeForm, OfficeReport, OfficeSeeker


@permission('office_index')
def index():
    allowed_office_ids = None

    if not current_user.is_admin():
        allowed_office_ids = current_user.allowed_office_id_list()

    form = OfficeSeeker(request.args)
    args = {
        "name": form.name.data if form.name.data != "" else None,
        "ids": current_user.allowed_office_id_list() if not current_user.is_admin() else None,
        "page": int(request.args.get('page', 1)),
        "per_page": Configuration.query.first().items_per_page
    }
    offices = Office.search_form(**args)

    return render_template("office/index.html", offices=offices, alert=get_alert(), form=form)


@permission('office_show')
def show(id):
    office = Office.get(id)
    if not office:
        add_alert(Alert("danger", "La oficina no existe."))
        return redirect(url_for("office_index"))

    return render_template("office/show.html", office=office)


@permission('office_create')
def new():
    return render_template("office/new.html", form=OfficeForm())


@permission('office_create')
def create():
    form = OfficeForm(id=None)
    if form.validate_on_submit():
        office = Office(name=form.name.data, email=form.email.data,
                        phone=form.phone.data, location=form.location.data)
        office.save()
        add_alert(
            Alert("success", f'La oficina "{office.name}" se ha creado correctamente.'))
        return redirect(url_for("office_index"))
    return render_template("office/new.html", form=form)


@permission('office_update')
def edit(id):
    office = Office.get(id)
    if not office:
        add_alert(Alert("danger", "La oficina no existe."))
        return redirect(url_for("office_index"))

    form = OfficeForm(obj=office)

    return render_template("office/edit.html", office=office, form=form)


@permission('office_update')
def update(id):
    office = Office.get(id)
    if not office:
        add_alert(Alert("danger", "La oficina no existe."))
        return redirect(url_for("office_index"))
    form = OfficeForm(id=id)
    if not form.validate_on_submit():
        return render_template("office/edit.html", office=office, form=form)
    office.update(name=form.name.data, email=form.email.data,
                  phone=form.phone.data, location=form.location.data)
    add_alert(
        Alert("success", f'La oficina "{office.name}" se ha modificado correctamente.'))
    return redirect(url_for("office_index"))


@permission('office_delete')
def delete(id):
    office = Office.get(id)
    if not office or office.is_deleted:
        add_alert(Alert("danger", "La oficina no existe."))
    elif office.has_active_charge():
        add_alert(Alert("danger", "La oficina no debe poseer cargos activos"))
    elif office.has_users():
        add_alert(Alert("danger", "La oficina no debe poseer responsables"))
    else:
        office.remove()
        add_alert(
            Alert("success", f'La oficina "{office.name}" se ha borrado correctamente.'))
    return redirect(url_for("office_index"))


@permission('office_report')
def report():

    form = OfficeReport(request.args)
    args = {
        "offices": form.offices.data,
        "charges_ids": form.charges.data,
        "institutional_email": form.institutional_email.data if form.institutional_email.data != "" else None,
        "name": form.name.data if form.name.data != "" else None,
        "surname": form.surname.data if form.surname.data != "" else None,
        "secondary_email": form.secondary_email.data if form.secondary_email.data != "" else None,
        "dni": form.dni.data if form.dni.data != "" else None
    }

    offices = []
    if current_user.is_admin() or current_user.is_visitante():
        offices = Office.all()
    else:
        offices = current_user.get_offices()
    form.offices.choices = offices.collect(
        lambda each: (each.id, each.name))
    form.charges.choices = Charge.all().select(lambda each: not each.is_docent).collect(
        lambda each: (each.id, each.name))

    offices_staff = []
    json_export = {}
    if request.args:
        data = Office.search(
            form.show_dni.data, form.show_secondary_email.data, **args)
        offices_staff = data["office_list"]
        json_export = data["staff_json"]

    return render_template("office/report.html", json_export=json_export, offices=offices_staff, dni_field=form.show_dni.data, secondary_email_field=form.show_secondary_email.data, form=form)
