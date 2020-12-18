
from flask import redirect, render_template, request, url_for
from flask_login import current_user

from app.helpers.previous_path import get_previous_path
from app.models.configuration import Configuration
from app.models.alert import Alert
from app.helpers.alert import add_alert, get_alert
from app.helpers.permission import permission
from app.models import Employee, Docent, NotDocent, Administrative, PendingEmployee
from app.helpers.forms import EmployeeForm
from app.helpers.previous_path import add_previous_path


@permission('employee_index')
def index():
    allowed_employee_ids = None

    if not current_user.is_admin():
        allowed_employee_ids = current_user.allowed_employee_id_list()

    employees = Employee.all_paginated(page=int(request.args.get('page', 1)),
                                       per_page=Configuration.get().items_per_page, ids=allowed_employee_ids)

    add_previous_path({"url": 'employee_index'})
    return render_template("employee/index.html", employees=employees, alert=get_alert())


@permission('employee_show')
def show(id):
    employee = Employee.get(id)
    if not employee:
        add_alert(Alert("danger", "El empleado no existe."))
        return redirect(url_for("employee_index"))

    return render_template("employee/show.html", employee=employee)


@permission('employee_create')
def new():
    return render_template("employee/new.html", form=EmployeeForm())


@permission('employee_create')
def create():

    form = EmployeeForm(id=None)

    if not form.validate_on_submit():
        return render_template("employee/new.html", form=form)

    if not current_user.is_admin():

        employee = PendingEmployee(
            name=form.name.data,
            surname=form.surname.data,
            dni=form.dni.data,
            institutional_email=form.institutional_email.data,
            secondary_email=form.secondary_email.data,
            type=form.type.data
        )
        employee.save()
        add_alert(Alert(
            "success", f'El empleado "{employee.name} {employee.surname}" quedo pendiente de aprobación.'))

    else:

        employee = Employee(
            name=form.name.data,
            surname=form.surname.data,
            dni=form.dni.data,
            institutional_email=form.institutional_email.data,
            secondary_email=form.secondary_email.data,
            type=form.type.data
        )
        employee.save()
        add_alert(Alert(
            "success", f'El empleado "{employee.name} {employee.surname}" se ha creado correctamente.'))

    previous_path = get_previous_path()
    if previous_path:
        if "args" in previous_path:
            return redirect(url_for(previous_path["url"], **previous_path["args"]))
        return redirect(url_for(previous_path["url"]))
    if not current_user.is_admin():
        redirect(url_for("cathedra_index"))
    return redirect(url_for("employee_index"))


@permission('employee_update')
def edit(id):
    employee = Employee.get(id)
    if not employee:
        add_alert(Alert("danger", "El empleado no existe."))
        return redirect(url_for("employee_index"))

    form = EmployeeForm(obj=employee)

    return render_template("employee/edit.html", employee=employee, form=form)


@permission('employee_update')
def update(id):
    employee = Employee.get(id)
    if not employee:
        add_alert(Alert("danger", "El empleado no existe."))
        return redirect(url_for("employee_index"))

    form = EmployeeForm(id=id, type=1)  # Linea de utilidad por el momento
    if not form.validate_on_submit():
        return render_template("employee/edit.html", employee=employee, form=form)

    if not current_user.is_admin():
        pending_employee = PendingEmployee(
            name=form.name.data,
            surname=form.surname.data,
            dni=form.dni.data,
            institutional_email=form.institutional_email.data,
            secondary_email=form.secondary_email.data,
            linked_employee=employee
        )
        pending_employee.save()
        add_alert(Alert(
            "success", f'Los cambios realizados sobre el empleado "{employee.name} {employee.surname}" quedaron pendientes de aprobación.'))
    else:
        employee.update(
            name=form.name.data,
            surname=form.surname.data,
            dni=form.dni.data,
            institutional_email=form.institutional_email.data,
            secondary_email=form.secondary_email.data
        )
        add_alert(Alert(
            "success", f'El empleado "{employee.name} {employee.surname}" se ha modificado correctamente.'))
    return redirect(url_for("employee_index"))


@permission('employee_delete')
def delete(id):
    employee = Employee.get(id)
    if not employee or employee.is_deleted:
        add_alert(Alert("danger", "El empleado no existe."))
    else:
        employee.remove()
        add_alert(
            Alert("success", f'El empleado "{employee.name} {employee.surname}" se ha borrado correctamente.'))
    return redirect(url_for("employee_index"))
