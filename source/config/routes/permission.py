
from app.resources import permission

def set_routes(app):

    app.add_url_rule("/permissions", "permission_index", permission.index)
    app.add_url_rule("/permission/show/<int:id>", "permission_show", permission.show)
    app.add_url_rule("/permission/new", "permission_new", permission.new)
    app.add_url_rule("/permission/create", "permission_create", permission.create, methods=["POST"])
    app.add_url_rule("/permission/edit/<int:id>", "permission_edit", permission.edit)
    app.add_url_rule("/permission/update/<int:id>", "permission_update", permission.update, methods=["POST"])
    app.add_url_rule("/permission/delete/<int:id>", "permission_delete", permission.delete)
