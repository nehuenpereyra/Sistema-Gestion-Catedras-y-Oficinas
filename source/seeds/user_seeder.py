
from flask_seeder import Seeder
from werkzeug.security import generate_password_hash

from app.models.user import User
from app.models.user_role import UserRole


class UserSeeder(Seeder):

    def __init__(self, db=None):
        super().__init__(db=db)
        self.priority = 3

    def run(self):
        print("[UserSeeder]")
        roles = {each.name: each for each in UserRole.query.all()}

        admin_user = User(name="Juan", surname="Lopez", email="admin@admin.com",
                          username="Juanchuz", password=generate_password_hash("admin123"),
                          roles=[roles["Administrador"]])
        admin_user.save()
        print(f" - {admin_user.username} user OK")

        operator_user = User(name="Lisa", surname="Gomez", email="lisa@gmail.com",
                             username="lisa", password=generate_password_hash("lisa123"),
                             roles=[roles["Operador"]])
        operator_user.save()
        print(f" - {operator_user.username} user OK")
