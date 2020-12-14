
from app.resources import request_type

def set_routes(app):

    app.add_url_rule("/request_types", "request_type_index", request_type.index)
    app.add_url_rule("/request_type/show/<int:id>", "request_type_show", request_type.show)
    app.add_url_rule("/request_type/new", "request_type_new", request_type.new)
    app.add_url_rule("/request_type/create", "request_type_create", request_type.create, methods=["POST"])
    app.add_url_rule("/request_type/edit/<int:id>", "request_type_edit", request_type.edit)
    app.add_url_rule("/request_type/update/<int:id>", "request_type_update", request_type.update, methods=["POST"])
    app.add_url_rule("/request_type/delete/<int:id>", "request_type_delete", request_type.delete)
