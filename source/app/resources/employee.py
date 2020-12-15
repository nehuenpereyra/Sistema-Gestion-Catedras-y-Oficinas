
from flask import redirect, render_template, request, url_for
from flask_login import current_user

from app.models.configuration import Configuration
from app.models.alert import Alert
from app.helpers.alert import add_alert, get_alert
from app.helpers.permission import permission
from app.models import Employee
from app.helpers.forms import EmployeeForm

@permission('employee_index')
def index():
    allowed_employee_ids = None

    if not current_user.is_admin():
        allowed_employee_ids = current_user.allowed_employee_id_list()

    employees = Employee.all_paginated(page=int(request.args.get('page', 1)),
                        per_page=Configuration.get().items_per_page, ids=allowed_employee_ids)
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
    if form.validate_on_submit():
        employee = Employee(name = form.name.data, surname = form.surname.data, dni = form.dni.data, institutional_email = form.institutional_email.data, secondary_email = form.secondary_email.data)
        employee.save()
        add_alert(
            Alert("success", f'El empleado "{employee.name}" se ha creado correctamente.'))
        return redirect(url_for("employee_index"))
    return render_template("employee/new.html", form=form)

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
    form = EmployeeForm(id=id)
    if not form.validate_on_submit():
        return render_template("employee/edit.html", employee=employee, form=form)
    employee.update(name = form.name.data, surname = form.surname.data, dni = form.dni.data, institutional_email = form.institutional_email.data, secondary_email = form.secondary_email.data)
    add_alert(
        Alert("success", f'El empleado "{employee.name}" se ha modificado correctamente.'))
    return redirect(url_for("employee_index"))

@permission('employee_delete')
def delete(id):
    employee = Employee.get(id)
    if not employee or employee.is_deleted:
        add_alert(Alert("danger", "El empleado no existe."))
    else:
        employee.remove()
        add_alert(
                Alert("success", f'El empleado "{employee.name}" se ha borrado correctamente.'))
    return redirect(url_for("employee_index"))