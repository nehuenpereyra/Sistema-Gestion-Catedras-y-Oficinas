from flask import render_template


def not_found_error(e):
    kwargs = {
        "error_name": "404 Not Found Error",
        "error_description": "La url a la que quiere acceder no existe",
    }
    return render_template("error.html", **kwargs), 404


def unauthorized_error(e):
    kwargs = {
        "error_name": "401 Unauthorized Error",
        "error_description": "No está autorizado para acceder a la url",
    }
    return render_template("error.html", **kwargs), 401


def forbidden_error(e):
    kwargs = {
        "error_name": "403 You don't have permission for this",
        "error_description": "No tienes permiso para esto",
    }
    return render_template("error.html", **kwargs), 403


def bad_request_error(e):
    kwargs = {
        "error_name": "400 One of the parameters specified in the request was invalid.",
        "error_description": "Uno de los parámetros especificados en la solicitud no es válido.",
    }
    return render_template("error.html", **kwargs), 400


def internal_server_error(e):
    kwargs = {
        "error_name": "500 Internal Server Error.",
        "error_description": "Uno de los parámetros especificados en la solicitud no es válido.",
    }
    return render_template("error.html", **kwargs), 500
