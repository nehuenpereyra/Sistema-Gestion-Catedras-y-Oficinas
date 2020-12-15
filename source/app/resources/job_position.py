
from flask import redirect, render_template, request, url_for
from flask_login import current_user

from app.models.configuration import Configuration
from app.models.alert import Alert
from app.helpers.alert import add_alert, get_alert
from app.helpers.permission import permission
from app.models import JobPosition, Charge, Cathedra, Employee
from app.helpers.forms import JobPositionForm

@permission('job_position_index')
def index():
    allowed_job_position_ids = None

    if not current_user.is_admin():
        allowed_job_position_ids = current_user.allowed_job_position_id_list()

    job_positions = JobPosition.all_paginated(page=int(request.args.get('page', 1)),
                        per_page=Configuration.get().items_per_page, ids=allowed_job_position_ids)
    return render_template("job_position/index.html", job_positions=job_positions, alert=get_alert())


@permission('job_position_show')
def show(id):
    job_position = JobPosition.get(id)
    if not job_position:
        add_alert(Alert("danger", "El puesto de trabajo no existe."))
        return redirect(url_for("job_position_index"))

    return render_template("job_position/show.html", job_position=job_position)

@permission('job_position_create')
def new():
    return render_template("job_position/new.html", form=JobPositionForm())

@permission('job_position_create')
def create():
    form = JobPositionForm(id=None)
    if form.validate_on_submit():
        job_position = JobPosition(start_date = form.start_date.data, end_date = form.end_date.data, charge = Charge.get(form.charge.data), cathedra = Cathedra.get(form.cathedra.data), employee = Employee.get(form.employee.data))
        job_position.save()
        add_alert(
            Alert("success", f'El puesto de trabajo "{job_position.start_date}" se ha creado correctamente.'))
        return redirect(url_for("job_position_index"))
    return render_template("job_position/new.html", form=form)

@permission('job_position_update')
def edit(id):
    job_position = JobPosition.get(id)
    if not job_position:
        add_alert(Alert("danger", "El puesto de trabajo no existe."))
        return redirect(url_for("job_position_index"))

    form = JobPositionForm(obj=job_position)
    form.charge.data = job_position.charge.id    
    form.cathedra.data = job_position.cathedra.id    
    form.employee.data = job_position.employee.id    

    return render_template("job_position/edit.html", job_position=job_position, form=form)

@permission('job_position_update')
def update(id):
    job_position = JobPosition.get(id)
    if not job_position:
        add_alert(Alert("danger", "El puesto de trabajo no existe."))
        return redirect(url_for("job_position_index"))
    form = JobPositionForm(id=id)
    if not form.validate_on_submit():
        return render_template("job_position/edit.html", job_position=job_position, form=form)
    job_position.update(start_date = form.start_date.data, end_date = form.end_date.data, charge = Charge.get(form.charge.data), cathedra = Cathedra.get(form.cathedra.data), employee = Employee.get(form.employee.data))
    add_alert(
        Alert("success", f'El puesto de trabajo "{job_position.start_date}" se ha modificado correctamente.'))
    return redirect(url_for("job_position_index"))

@permission('job_position_delete')
def delete(id):
    job_position = JobPosition.get(id)
    if not job_position or job_position.is_deleted:
        add_alert(Alert("danger", "El puesto de trabajo no existe."))
    else:
        job_position.remove()
        add_alert(
                Alert("success", f'El puesto de trabajo "{job_position.start_date}" se ha borrado correctamente.'))
    return redirect(url_for("job_position_index"))