
from app.resources import charge

def set_routes(app):

    app.add_url_rule("/charges", "charge_index", charge.index)
    app.add_url_rule("/charge/show/<int:id>", "charge_show", charge.show)
    app.add_url_rule("/charge/new", "charge_new", charge.new)
    app.add_url_rule("/charge/create", "charge_create", charge.create, methods=["POST"])
    app.add_url_rule("/charge/edit/<int:id>", "charge_edit", charge.edit)
    app.add_url_rule("/charge/update/<int:id>", "charge_update", charge.update, methods=["POST"])
    app.add_url_rule("/charge/delete/<int:id>", "charge_delete", charge.delete)
