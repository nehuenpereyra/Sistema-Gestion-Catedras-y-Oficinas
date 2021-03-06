from flask import redirect, render_template, request, url_for
from flask_login import current_user
from datetime import datetime

from app.models.configuration import Configuration
from app.models.alert import Alert
from app.helpers.previous_path import add_previous_path
from app.helpers.alert import add_alert, get_alert
from app.helpers.permission import permission
from app.models import JobPosition, Charge, Cathedra, Office, Employee, Workplace, Docent, NotDocent, Administrative
from app.helpers.forms import JobPositionForm


@permission('job_position_index')
def index(workplace_id):
    allowed_job_position_ids = None
    workplace = Workplace.get(workplace_id)

    if not current_user.is_admin():
        allowed_job_position_ids = current_user.allowed_job_position_id_list()

    job_positions = JobPosition.all_paginated(page=int(request.args.get('page', 1)),
                                              per_page=Configuration.get().items_per_page, ids=allowed_job_position_ids)
    add_previous_path({"url": 'job_position_index', "args": {
                      "workplace_id": workplace_id}})
    return render_template("job_position/index.html", staff=workplace.sttaf_json(), job_positions=job_positions, workplace_id=workplace_id, is_cathedra=workplace.is_cathedra(), workplace_name=workplace.name, alert=get_alert())


@ permission('job_position_show')
def show(workplace_id, id):
    job_position = JobPosition.get(id)
    if not job_position or not job_position.is_active():
        add_alert(Alert("danger", "El puesto de trabajo no existe."))
        return redirect(url_for("job_position_index", workplace_id=workplace_id))

    return render_template("job_position/show.html", workplace_id=workplace_id, job_position=job_position)


@ permission('job_position_create')
def new(workplace_id, type):
    workplace = Workplace.get(workplace_id)
    form = JobPositionForm()
    if workplace.is_cathedra():
        if type == 'docent':
            form.charge.choices = Charge.find_by_is_docent(
                True).collect(lambda each: (each.id, each.name))
            form.employee.choices = list(set(workplace.all_docent()) ^ set(Docent.all())).collect(
                lambda each: (each.id, each.get_full_name()))
        else:
            form.charge.choices = Charge.find_by_is_docent(
                False).collect(lambda each: (each.id, each.name))
            form.employee.choices = list(set(workplace.all_not_docent()) ^ set(NotDocent.all())).collect(
                lambda each: (each.id, each.get_full_name()))
    else:
        form.charge.choices = Charge.find_by_is_docent(
            False).collect(lambda each: (each.id, each.name))
        form.employee.choices = list(set(workplace.all_administrative()) ^ set(Administrative.all())).collect(
            lambda each: (each.id, each.get_full_name()))

    return render_template("job_position/new.html", workplace_id=workplace_id, type=type, form=form)


@ permission('job_position_create')
def create(workplace_id):
    form = JobPositionForm(id=None)
    if form.validate_on_submit():
        job_position = JobPosition(
            start_date=datetime.today(),
            end_date=None,
            charge=Charge.get(form.charge.data),
            workplace=Workplace.get(workplace_id),
            employee=Employee.get(form.employee.data),
            review=not current_user.is_admin()
        )
        job_position.save()
        add_alert(
            Alert("success", f'Se agreg?? a "{job_position.employee.get_full_name()}" al plantel correctamente.'))
        return redirect(url_for("job_position_index", workplace_id=workplace_id))
    return render_template("job_position/new.html", workplace_id=workplace_id, form=form)


@ permission('job_position_update')
def edit(workplace_id, id):
    job_position = JobPosition.get(id)
    workplace = Workplace.get(workplace_id)
    if not job_position or not job_position.is_active():
        add_alert(Alert("danger", "El puesto de trabajo no existe."))
        return redirect(url_for("job_position_index", workplace_id=workplace_id))

    form = JobPositionForm(obj=job_position)
    if workplace.is_cathedra() and job_position.employee.is_docent():
        form.charge.choices = Charge.find_by_is_docent(
            True).collect(lambda each: (each.id, each.name))
    else:
        form.charge.choices = Charge.find_by_is_docent(
            False).collect(lambda each: (each.id, each.name))
    form.charge.data = job_position.charge.id
    form.employee.data = job_position.employee.id
    return render_template("job_position/edit.html", workplace_id=workplace_id, job_position=job_position, form=form)


@ permission('job_position_update')
def update(workplace_id, id):
    job_position = JobPosition.get(id)
    if not job_position or not job_position.is_active():
        add_alert(Alert("danger", "El puesto de trabajo no existe."))
        return redirect(url_for("job_position_index", workplace_id=workplace_id))
    form = JobPositionForm(id=id)
    form.employee.data = job_position.employee.id
    if not form.validate_on_submit():
        return render_template("job_position/edit.html", workplace_id=workplace_id, job_position=job_position, form=form)

    # job_position.update(start_date=datetime.today(), end_date=None, charge=Charge.get(
    #    form.charge.data), workplace=Workplace.get(workplace_id), employee=Employee.get(form.employee.data))

    new_charge = Charge.get(form.charge.data)

    if new_charge is not job_position.charge:
        job_position.reassign(new_charge, review=not current_user.is_admin())
        job_position.save()

    add_alert(
        Alert("success", f'Se modific?? el cargo de "{job_position.employee.get_full_name()}" correctamente.'))
    return redirect(url_for("job_position_index", workplace_id=workplace_id))


@ permission('job_position_delete')
def delete(workplace_id, id):
    job_position = JobPosition.get(id)
    if not job_position or not job_position.is_active():
        add_alert(Alert("danger", "El puesto de trabajo no existe."))
    else:
        job_position.finish(review=not current_user.is_admin())
        add_alert(
            Alert("success", f'Se quito a "{job_position.employee.get_full_name()}" del plantel correctamente.'))
    return redirect(url_for("job_position_index", workplace_id=workplace_id))
