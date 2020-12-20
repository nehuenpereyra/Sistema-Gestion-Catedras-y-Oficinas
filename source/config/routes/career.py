
from app.resources import career


def set_routes(app):

    app.add_url_rule("/careers", "career_index", career.index)
    app.add_url_rule("/career/show/<int:id>", "career_show", career.show)
    app.add_url_rule("/career/new", "career_new", career.new)
    app.add_url_rule("/career/create", "career_create",
                     career.create, methods=["POST"])
    app.add_url_rule("/career/edit/<int:id>", "career_edit", career.edit)
    app.add_url_rule("/career/update/<int:id>", "career_update",
                     career.update, methods=["POST"])
    app.add_url_rule("/career/delete/<int:id>", "career_delete", career.delete)
    app.add_url_rule("/career/report", "career_report",
                     career.report, methods=["GET", "POST"])
