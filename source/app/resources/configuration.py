from flask import redirect, render_template, request, url_for, abort, jsonify
from flask_login import login_required

from app.helpers.permission import permission
from app.helpers.forms.configuration_form import ConfigurationForm
from app.helpers.alert import add_alert
from app.models.configuration import Configuration
from app.models.alert import Alert


@permission('configuration_update')
def edit():
    config = Configuration.query.all()[0]
    form = ConfigurationForm(obj=config)
    return render_template("configuration/update.html", form=form)



@permission('configuration_update')
def update():
    form = ConfigurationForm()
    if form.validate_on_submit():
        Configuration.update(title=form.title.data, description=form.description.data, contact_email=form.contact_email.data,
                             pagination_elements=form.pagination_elements.data, enabled_site=form.enabled_site.data)
        add_alert(
            Alert("success", f"La configuración se actualizo correctamente."))
        return redirect(url_for("index"))
    return render_template("configuration/update.html", form=form)
