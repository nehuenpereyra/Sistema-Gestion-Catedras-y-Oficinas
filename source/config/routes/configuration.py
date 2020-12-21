from app.resources import configuration


def set_routes(app):
    app.add_url_rule("/configuration", "configuration_update",
                     configuration.update, methods=["POST"])
    app.add_url_rule("/configuration/edit",
                     "configuration_edit", configuration.edit)
