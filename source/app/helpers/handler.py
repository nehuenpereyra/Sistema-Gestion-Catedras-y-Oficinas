from flask import render_template


def not_found_error(e):
    kwargs = {
        "error_code": 404,
        "error_description": "El servidor no pudo encontrar el contenido solicitado",
    }
    return render_template("error.html", **kwargs), 404


def unauthorized_error(e):
    kwargs = {
        "error_code": 401,
        "error_description": "No está autorizado para acceder al recurso solicitado",
    }
    return render_template("error.html", **kwargs), 401


def forbidden_error(e):
    kwargs = {
        "error_code": 403,
        "error_description": "No tienes permiso para esto",
    }
    return render_template("error.html", **kwargs), 403


def bad_request_error(e):
    kwargs = {
        "error_code": 400,
        "error_description": "Uno de los parámetros especificados en la solicitud no es válido.",
    }
    return render_template("error.html", **kwargs), 400


def internal_server_error(e):
    kwargs = {
        "error_code": 500,
        "error_description": "Uno de los parámetros especificados en la solicitud no es válido.",
    }
    return render_template("error.html", **kwargs), 500
