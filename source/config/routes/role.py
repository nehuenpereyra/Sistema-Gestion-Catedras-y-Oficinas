
from app.resources import role

def set_routes(app):

    app.add_url_rule("/roles", "role_index", role.index)
    app.add_url_rule("/role/show/<int:id>", "role_show", role.show)
    app.add_url_rule("/role/new", "role_new", role.new)
    app.add_url_rule("/role/create", "role_create", role.create, methods=["POST"])
    app.add_url_rule("/role/edit/<int:id>", "role_edit", role.edit)
    app.add_url_rule("/role/update/<int:id>", "role_update", role.update, methods=["POST"])
    app.add_url_rule("/role/delete/<int:id>", "role_delete", role.delete)
