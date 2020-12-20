
from flask import redirect, render_template, request, url_for
from flask_login import current_user

from app.models.configuration import Configuration
from app.models.alert import Alert
from app.helpers.alert import add_alert, get_alert
from app.helpers.permission import permission
from app.models import Charge
from app.helpers.forms import ChargeForm, ChargeSeeker


@permission('charge_index')
def index():
    allowed_charge_ids = None

    if not current_user.is_admin():
        allowed_charge_ids = current_user.allowed_charge_id_list()

    form = ChargeSeeker(request.args)
    args = {
        "name": form.name.data if form.name.data != "" else None,
        "charge_type": form.charge_type.data,
        "page": int(request.args.get('page', 1)),
        "per_page": Configuration.query.first().items_per_page
    }
    charges = Charge.search(**args)

    return render_template("charge/index.html", charges=charges, alert=get_alert(), form=form)


@permission('charge_show')
def show(id):
    charge = Charge.get(id)
    if not charge:
        add_alert(Alert("danger", "El cargo no existe."))
        return redirect(url_for("charge_index"))

    return render_template("charge/show.html", charge=charge)


@permission('charge_create')
def new():
    return render_template("charge/new.html", form=ChargeForm())


@permission('charge_create')
def create():
    form = ChargeForm(id=None)
    if form.validate_on_submit():
        charge = Charge(name=form.name.data,
                        is_docent=form.is_docent.data, order=form.order.data)
        charge.save()
        add_alert(
            Alert("success", f'El cargo "{charge.name}" se ha creado correctamente.'))
        return redirect(url_for("charge_index"))
    return render_template("charge/new.html", form=form)


@permission('charge_update')
def edit(id):
    charge = Charge.get(id)
    if not charge:
        add_alert(Alert("danger", "El cargo no existe."))
        return redirect(url_for("charge_index"))

    form = ChargeForm(obj=charge)

    return render_template("charge/edit.html", charge=charge, form=form)


@permission('charge_update')
def update(id):
    charge = Charge.get(id)
    if not charge:
        add_alert(Alert("danger", "El cargo no existe."))
        return redirect(url_for("charge_index"))
    form = ChargeForm(id=id)
    if not form.validate_on_submit():
        return render_template("charge/edit.html", charge=charge, form=form)
    charge.update(name=form.name.data,
                  is_docent=form.is_docent.data, order=form.order.data)
    add_alert(
        Alert("success", f'El cargo "{charge.name}" se ha modificado correctamente.'))
    return redirect(url_for("charge_index"))


@permission('charge_delete')
def delete(id):
    charge = Charge.get(id)
    if not charge or charge.is_deleted:
        add_alert(Alert("danger", "El cargo no existe."))
    else:
        charge.remove()
        add_alert(
            Alert("success", f'El cargo "{charge.name}" se ha borrado correctamente.'))
    return redirect(url_for("charge_index"))
