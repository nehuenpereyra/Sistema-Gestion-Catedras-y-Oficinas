from flask import redirect, render_template, request, url_for, abort, jsonify
from flask_login import login_required

from app.helpers.permission import permission
from app.helpers.forms.configuration_form import ConfigurationForm
from app.helpers.alert import add_alert
from app.models.configuration import Configuration
from app.models.alert import Alert


@permission('configuration_update')
def edit():
    config = Configuration.get()
    form = ConfigurationForm(obj=config)
    return render_template("configuration/update.html", form=form)


@permission('configuration_update')
def update():
    form = ConfigurationForm()
    if form.validate_on_submit():
        Configuration.update(mail_server=form.mail_server.data,
                             mail_port=form.mail_port.data,
                             contact_email=form.mail_contact.data,
                             items_per_page=form.items_per_page.data,
                             mail_password=form.mail_password.data)
        add_alert(
            Alert("success", f"La configuración se actualizo correctamente."))
        return redirect(url_for("index"))
    return render_template("configuration/update.html", form=form)
