
from app.resources import office


def set_routes(app):

    app.add_url_rule("/offices", "office_index", office.index)
    app.add_url_rule("/office/show/<int:id>", "office_show", office.show)
    app.add_url_rule("/office/new", "office_new", office.new)
    app.add_url_rule("/office/create", "office_create",
                     office.create, methods=["POST"])
    app.add_url_rule("/office/edit/<int:id>", "office_edit", office.edit)
    app.add_url_rule("/office/update/<int:id>", "office_update",
                     office.update, methods=["POST"])
    app.add_url_rule("/office/delete/<int:id>", "office_delete", office.delete)
    app.add_url_rule("/office/report", "office_report",
                     office.report, methods=["GET", "POST"])
