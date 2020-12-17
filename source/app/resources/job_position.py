import bisect 
from flask import redirect, render_template, request, url_for
from flask_login import current_user
from datetime import datetime

from app.models.configuration import Configuration
from app.models.alert import Alert
from app.helpers.alert import add_alert, get_alert
from app.helpers.permission import permission
from app.models import JobPosition, Charge, Cathedra, Office, Employee, Workplace, Docent, NotDocent, Administrative
from app.helpers.forms import JobPositionForm

class ChargeEmployees:
    def __init__(self, charge, employees):
        self.charge = charge
        self.employees = employees
    def __lt__(self, other):
        return self.charge.order < other.charge.order


@permission('job_position_index')
def index(workplace_id):
    allowed_job_position_ids = None

    workplace = Workplace.get(workplace_id)
    staff = {}
    charge = {}
    # for personal_staff in workplace.staff:
    #     if personal_staff.isActive():
    #         if not personal_staff.charge in charge:
    #             charge[personal_staff.charge] = []
    #         charge[personal_staff.charge] = charge[personal_staff.charge].add(personal_staff.employee)
    # for key, value in charge.items():
    #     print(key)
    #     print(value)
    #     if not value is None:
    #         if not value in staff:
    #             staff[value.get_label()] = []
    #         bisect.insort(staff[value.get_label()], ChargeEmployees(key, value)) 

    #print(staff['Administrativo'][0].charge)        
    #print(staff['Administrativo'][0].employees)
    if not current_user.is_admin():
        allowed_job_position_ids = current_user.allowed_job_position_id_list()

    job_positions = JobPosition.all_paginated(page=int(request.args.get('page', 1)),
                        per_page=Configuration.get().items_per_page, ids=allowed_job_position_ids)
    return render_template("job_position/index.html", job_positions=job_positions, workplace_id=workplace_id, alert=get_alert())


@permission('job_position_show')
def show(workplace_id, id):
    job_position = JobPosition.get(id)
    if not job_position:
        add_alert(Alert("danger", "El puesto de trabajo no existe."))
        return redirect(url_for("job_position_index"))

    return render_template("job_position/show.html", workplace_id=workplace_id, job_position=job_position)

@permission('job_position_create')
def new(workplace_id):
    workplace = Workplace.get(workplace_id)
    form = JobPositionForm()
    if workplace.is_cathedra():
        form.charge.choices = Charge.find_by_is_docent(True).collect(lambda each: (each.id, each.name))
        form.employee.choices = (Docent.all() + NotDocent.all()).collect(lambda each: (each.id, each.name))
    else:
        form.charge.choices = Charge.find_by_is_docent(False).collect(lambda each: (each.id, each.name))
        form.employee.choices  = Administrative.all().collect(lambda each: (each.id, each.name))
    
    return render_template("job_position/new.html", workplace_id=workplace_id, form=form)

@permission('job_position_create')
def create(workplace_id):
    form = JobPositionForm(id=None)
    if form.validate_on_submit():
        job_position = JobPosition(start_date = datetime.today(), end_date = None, charge = Charge.get(form.charge.data), workplace = Workplace.get(workplace_id), employee = Employee.get(form.employee.data))
        job_position.save()
        add_alert(
            Alert("success", f'El puesto de trabajo "{job_position.start_date}" se ha creado correctamente.'))
        return redirect(url_for("job_position_index", workplace_id=workplace_id))
    return render_template("job_position/new.html", workplace_id=workplace_id, form=form)

@permission('job_position_update')
def edit(workplace_id, id):
    job_position = JobPosition.get(id)
    workplace = Workplace.get(workplace_id)
    if not job_position:
        add_alert(Alert("danger", "El puesto de trabajo no existe."))
        return redirect(url_for("job_position_index", workplace_id=workplace_id))

    form = JobPositionForm(obj=job_position)
    if workplace.is_cathedra():
        form.charge.choices = Charge.find_by_is_docent(True).collect(lambda each: (each.id, each.name))
    else:
        form.charge.choices = Charge.find_by_is_docent(False).collect(lambda each: (each.id, each.name))
    form.charge.data = job_position.charge.id
    form.employee.data = job_position.employee.id
    return render_template("job_position/edit.html", workplace_id=workplace_id, job_position=job_position, form=form)

@permission('job_position_update')
def update(workplace_id, id):
    job_position = JobPosition.get(id)
    if not job_position:
        add_alert(Alert("danger", "El puesto de trabajo no existe."))
        return redirect(url_for("job_position_index", workplace_id=workplace_id))
    form = JobPositionForm(id=id)
    form.employee.data = job_position.employee.id
    if not form.validate_on_submit():
        return render_template("job_position/edit.html", workplace_id=workplace_id, job_position=job_position, form=form)
    job_position.update(start_date = datetime.today(), end_date = None, charge = Charge.get(form.charge.data), workplace = Workplace.get(workplace_id), employee = Employee.get(form.employee.data))
    add_alert(
        Alert("success", f'El puesto de trabajo "{job_position.start_date}" se ha modificado correctamente.'))
    return redirect(url_for("job_position_index", workplace_id=workplace_id))

@permission('job_position_delete')
def delete(workplace_id, id):
    job_position = JobPosition.get(id)
    if not job_position or job_position.is_deleted:
        add_alert(Alert("danger", "El puesto de trabajo no existe."))
    else:
        job_position.remove()
        add_alert(
                Alert("success", f'El puesto de trabajo "{job_position.start_date}" se ha borrado correctamente.'))
    return redirect(url_for("job_position_index", workplace_id=workplace_id))