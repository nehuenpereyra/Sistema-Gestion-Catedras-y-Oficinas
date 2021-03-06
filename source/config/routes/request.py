
from app.resources import request

def set_routes(app):

    app.add_url_rule("/requests", "request_index", request.index)
    app.add_url_rule("/request/show/<int:id>", "request_show", request.show)
    app.add_url_rule("/request/support", "request_support", request.support)
    app.add_url_rule("/request/create", "request_create", request.create, methods=["POST"])
    app.add_url_rule("/request/edit/<int:id>", "request_edit", request.edit)
    app.add_url_rule("/request/update/<int:id>", "request_update", request.update, methods=["POST"])
    app.add_url_rule("/request/solved/<int:id>", "request_solved", request.solved)
