
from flask import redirect, render_template, request, url_for
from flask_login import current_user

from app.models.configuration import Configuration
from app.models.alert import Alert
from app.helpers.alert import add_alert, get_alert
from app.helpers.permission import permission
from app.models import Career
from app.helpers.forms import CareerForm

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
        add_alert(Alert("danger", "El carrera no existe."))
        return redirect(url_for("career_index"))

    return render_template("career/show.html", career=career)

@permission('career_create')
def new():
    return render_template("career/new.html", form=CareerForm())

@permission('career_create')
def create():
    form = CareerForm(id=None)
    if form.validate_on_submit():
        career = Career(name = form.name.data)
        career.save()
        add_alert(
            Alert("success", f"El {career.name} se a creado correctamente."))
        return redirect(url_for("career_index"))
    return render_template("career/new.html", form=form)

@permission('career_update')
def edit(id):
    career = Career.get(id)
    if not career:
        add_alert(Alert("danger", "El carrera no existe."))
        return redirect(url_for("career_index"))

    form = CareerForm(obj=career)

    return render_template("career/edit.html", career=career, form=form)

@permission('career_update')
def update(id):
    career = Career.get(id)
    if not career:
        add_alert(Alert("danger", "El carrera no existe."))
        return redirect(url_for("career_index"))
    form = CareerForm(id=id)
    if not form.validate_on_submit():
        return render_template("career/edit.html", career=career, form=form)
    career.update(name = form.name.data)
    add_alert(
        Alert("success", f"El {career.name} se a modificado correctamente."))
    return redirect(url_for("career_index"))

@permission('career_delete')
def delete(id):
    career = Career.get(id)
    if not career or career.is_deleted:
        add_alert(Alert("danger", "El carrera no existe."))
    else:
        career.remove()
        add_alert(
                Alert("success", f"El {career.name} se a borrado correctamente."))
    return redirect(url_for("career_index"))