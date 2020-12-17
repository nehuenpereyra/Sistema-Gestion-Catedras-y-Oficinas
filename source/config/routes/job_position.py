
from app.resources import job_position

def set_routes(app):

    app.add_url_rule("/staff/<int:workplace_id>", "job_position_index", job_position.index)
    app.add_url_rule("/staff/<int:workplace_id>/show/<int:id>", "job_position_show", job_position.show)
    app.add_url_rule("/staff/<int:workplace_id>/new", "job_position_new", job_position.new)
    app.add_url_rule("/staff/<int:workplace_id>/create", "job_position_create", job_position.create, methods=["POST"])
    app.add_url_rule("/staff/<int:workplace_id>/edit/<int:id>", "job_position_edit", job_position.edit)
    app.add_url_rule("/staff/<int:workplace_id>/update/<int:id>", "job_position_update", job_position.update, methods=["POST"])
    app.add_url_rule("/staff/<int:workplace_id>/delete/<int:id>", "job_position_delete", job_position.delete)
