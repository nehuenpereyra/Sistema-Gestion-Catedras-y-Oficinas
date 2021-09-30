
from flask_seeder import Seeder
from werkzeug.security import generate_password_hash

from app.models import User, Role


class UserSeeder(Seeder):

    def __init__(self, db=None):
        super().__init__(db=db)
        self.priority = 3

    def run(self):
        print("[UserSeeder]")
        roles = {each.name: each for each in Role.query.all()}

        admin_user = User(name="Juan", surname="Lopez", institutional_email="admin@admin.com",
                          secondary_email="admin_secondary@admin.com", username="admin",
                          password="password")
        admin_user.set_roles([roles["Administrador"]])
        admin_user.save()
        print(f" - {admin_user.username} user OK")

        cathedra_manager = User(name="Lisa", surname="Gomez", institutional_email="operador@operador.com",
                                secondary_email="operador_secondary@operador.com", username="lisa",
                                password="password")
        cathedra_manager.set_roles([roles["Responsable de Catedra"]])
        cathedra_manager.save()
        print(f" - {cathedra_manager.username} user OK")
