
from flask import render_template, url_for, request, redirect

from app.models import Configuration, PendingEmployee
from app.models.alert import Alert
from app.helpers.alert import add_alert, get_alert
from app.helpers.permission import permission
from app.helpers.forms import EmployeeForm

@permission('pending_employee_index')
def index():
    employees = PendingEmployee.all_paginated(page=int(request.args.get('page', 1)),
                        per_page=Configuration.get().items_per_page)
    return render_template("employee/pending_index.html", employees=employees, alert=get_alert())

@permission('pending_employee_show')
def show(id):
    employee = PendingEmployee.get(id)
    if not employee:
        add_alert(Alert("danger", "El empleado pendiente de aprobación no existe."))
        return redirect(url_for("pending_employee_index"))

    return render_template("employee/pending_show.html", employee=employee)

@permission('pending_employee_accept')
def accept(id):
    employee = PendingEmployee.get(id)
    if not employee:
        add_alert(Alert("danger", "El empleado pendiente de aprobación no existe."))
        return redirect(url_for("pending_employee_index"))
    
    if employee.is_new():
        alert_message = 'El {} "{}" fue aceptado y agregado con exito.'.format(
            employee.get_label().lower(),
            employee.get_full_name()
        )
    else:
        alert_message = 'Los cambios pendientes del {} "{}" fueron aceptados y se actualizo con exito.'.format(
            employee.linked_employee.get_label().lower(),
            employee.linked_employee.get_full_name()
        )
    
    employee.accept()
    add_alert(Alert("success", alert_message))

    return redirect(url_for("pending_employee_index"))

@permission('pending_employee_reject')
def reject(id):
    employee = PendingEmployee.get(id)
    if not employee:
        add_alert(Alert("danger", "El empleado pendiente de aprobación no existe."))
        return redirect(url_for("pending_employee_index"))
    
    if employee.is_new():
        alert_message = 'El {} "{}" fue rechazado con exito.'.format(
            employee.get_label().lower(),
            employee.get_full_name()
        )
    else:
        alert_message = 'Los cambios pendientes del {} "{}" fueron rechazados con exito.'.format(
            employee.linked_employee.get_label().lower(),
            employee.linked_employee.get_full_name()
        )

    employee.reject()
    add_alert(Alert("success", alert_message))

    return redirect(url_for("pending_employee_index"))