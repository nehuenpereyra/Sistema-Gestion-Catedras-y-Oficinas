
from app.resources import cathedra

def set_routes(app):

    app.add_url_rule("/cathedras", "cathedra_index", cathedra.index)
    app.add_url_rule("/cathedra/show/<int:id>", "cathedra_show", cathedra.show)
    app.add_url_rule("/cathedra/new", "cathedra_new", cathedra.new)
    app.add_url_rule("/cathedra/create", "cathedra_create", cathedra.create, methods=["POST"])
    app.add_url_rule("/cathedra/edit/<int:id>", "cathedra_edit", cathedra.edit)
    app.add_url_rule("/cathedra/update/<int:id>", "cathedra_update", cathedra.update, methods=["POST"])
    app.add_url_rule("/cathedra/delete/<int:id>", "cathedra_delete", cathedra.delete)
