from app.resources import auth


def set_routes(app):
    app.add_url_rule("/login", "auth_login", auth.login)
    app.add_url_rule("/logout", "auth_logout", auth.logout)
    app.add_url_rule(
        "/authenticate", "auth_authenticate", auth.authenticate, methods=["POST"]
    )
