from app.resources import configuration


def set_routes(app):
    # Rutas de Configuracion
    app.add_url_rule("/configuracion", "configuration_update",
                     configuration.update, methods=["POST"])
    app.add_url_rule("/configuracion/editar",
                     "configuration_edit", configuration.edit)
