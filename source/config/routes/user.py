
from app.resources import user


def set_routes(app):

    app.add_url_rule("/users", "user_index", user.index)
    app.add_url_rule("/user/show/<int:id>", "user_show", user.show)
    app.add_url_rule("/user/new", "user_new", user.new)
    app.add_url_rule("/user/create", "user_create",
                     user.create, methods=["POST"])
    app.add_url_rule("/user/edit/<int:id>", "user_edit", user.edit)
    app.add_url_rule("/user/update/<int:id>", "user_update",
                     user.update, methods=["POST"])
    app.add_url_rule("/user/delete/<int:id>", "user_delete", user.delete)
    app.add_url_rule("/user/password_recovery", "user_password_recovery",
                     user.password_recovery, methods=["GET", "POST"])
    app.add_url_rule("/user/password_change/<string:url_recovery>", "user_password_change",
                     user.password_change, methods=["GET", "POST"])
