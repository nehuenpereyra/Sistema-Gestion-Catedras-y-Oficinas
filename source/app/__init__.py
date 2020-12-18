from os import path, environ

from flask import Flask
from flask_session import Session
from smallthon import sm_list
from flask_ckeditor import CKEditor

from app.db import set_db
from app.CKEditor import set_CKEditor
from config.config import config
from config.routes import set_routes
from app.helpers.login import set_login, authenticated
from app.helpers.permission import verify_permission
from app.helpers.view import show_field, link
from app.helpers.pagination import url_for_page


def create_app(environment="development"):

    # Configuración inicial de la app
    app = Flask(__name__)

    # Agrega el manejo se seciones
    app.config["SESSION_TYPE"] = "filesystem"
    Session(app)

    # Carga de la configuración
    env = environ.get("FLASK_ENV", "development")
    app.config.from_object(config[env])

    # Añade a la app flask login
    set_login(app)

    # Establece la db que posee la app
    set_db(app)

    # Funciones que se exportan al contexto de Jinja2
    app.jinja_env.globals.update(is_authenticated=authenticated)
    app.jinja_env.globals.update(verify_permission=verify_permission)
    app.jinja_env.globals.update(show_field=show_field)
    app.jinja_env.globals.update(link=link)
    app.jinja_env.globals.update(url_for_page=url_for_page)

    sm_list()

    # Se agrega la ruta por defecto para subir archivos a la configuracion
    app.config['UPLOAD_FOLDER'] = "app/static/uploads"

    # Se agrega la URL de la api de referencia a la configuracion
    app.config["REFERENCES_API_URL"] = "https://api-referencias.proyecto2020.linti.unlp.edu.ar"

    # Establece las rutas que posee la app
    set_routes(app)

    # Agrega a la aplicación el CKEditor
    set_CKEditor(app)

    # Retornar la instancia de app configurada
    return app
