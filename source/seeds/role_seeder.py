
from flask_seeder import Seeder

from app.models import Role, Permission


class RoleSeeder(Seeder):

    def __init__(self, db=None):
        super().__init__(db=db)
        self.priority = 2

    def run(self):
        print("[RoleSeeder]")
        permissions = {each.name: each for each in Permission.all()}

        admin_role = Role(name="Administrador", permissions=list(
            permissions.values()))
        admin_role.permissions.remove(permissions["request_create"])
        admin_role.permissions.remove(permissions["request_update"])
        admin_role.save()
        print(f" - {admin_role.name} Role OK")

        career_manager_role = Role(
            name="Responsable de Carrera", permissions=[
                permissions["user_show"],
                permissions["career_index"],
                permissions["career_show"],
                permissions["cathedra_index"],
                permissions["cathedra_show"],
                permissions["request_index"],
                permissions["request_show"],
                permissions["request_create"],
                permissions["employee_index"],
                permissions["employee_show"],
                permissions["employee_create"],
                permissions["employee_update"]
            ])
        career_manager_role.save()
        print(f" - {career_manager_role.name} Role OK")

        cathedra_manager_role = Role(
            name="Responsable de Catedra", permissions=[
                permissions["user_show"],
                permissions["cathedra_index"],
                permissions["cathedra_show"],
                permissions["request_index"],
                permissions["request_show"],
                permissions["request_create"],
                permissions["employee_index"],
                permissions["employee_show"],
                permissions["employee_create"],
                permissions["employee_update"]
            ])
        cathedra_manager_role.save()
        print(f" - {cathedra_manager_role.name} Role OK")

        office_manager_role = Role(
            name="Responsable de Oficina", permissions=[
                permissions["user_show"],
                permissions["office_index"],
                permissions["office_show"],
                permissions["request_index"],
                permissions["request_show"],
                permissions["request_create"],
                permissions["employee_index"],
                permissions["employee_show"],
                permissions["employee_create"],
                permissions["employee_update"]
            ])
        office_manager_role.save()
        print(f" - {office_manager_role.name} Role OK")

        visitor_role = Role(
            name="Visitante", permissions=[
                permissions["user_show"],
                permissions["request_index"],
                permissions["request_show"],
                permissions["request_create"],
            ])
        visitor_role.save()
        print(f" - {visitor_role.name} Role OK")
