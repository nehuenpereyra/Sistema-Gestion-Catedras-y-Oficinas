from flask_sqlalchemy import SQLAlchemy
from flask_seeder import FlaskSeeder

db = SQLAlchemy()  # Se crea un objeto de tipo SQLAlchemy
seeder = FlaskSeeder()  # Se crea un objeto de tipo FlaskSeeder

def set_db(app):
    # Configura la base de datos
    db.init_app(app)
    seeder.init_app(app, db)
    with app.app_context():  # Crea un contexto de aplicación
        db.create_all()  # Crea las tablas de la base de datos
