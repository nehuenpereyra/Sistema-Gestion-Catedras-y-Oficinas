from app.resources import user


def set_routes(app):
    # Rutas de Usuarios
    app.add_url_rule("/usuario/perfil", "user_profile", user.profile)
    app.add_url_rule("/usuarios/", "user_index", user.index)

    app.add_url_rule("/usuario/nuevo", "user_new", user.new)
    app.add_url_rule("/usuario/nuevo", "user_create",
                     user.create, methods=["POST"])

    app.add_url_rule("/usuario/editar/<int:id>", "user_edit", user.edit)
    app.add_url_rule("/usuario/actualizar/<int:id>", "user_update", user.update,
                     methods=["POST"])

    app.add_url_rule("/usuario/borrar/<int:id>", "user_delete", user.delete)
