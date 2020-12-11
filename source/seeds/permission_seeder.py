
from flask_seeder import Seeder

from app.models.user_permission import UserPermission


class PermissionSeeder(Seeder):

    def __init__(self, db=None):
        super().__init__(db=db)
        self.priority = 1

    def run(self):
        print("[PermissionSeeder]")

        UserPermission(name="configuration_update").save()
        print(f" - Configuration Permission OK")

        UserPermission(name="user_index").save()
        UserPermission(name="user_create").save()
        UserPermission(name="user_update").save()
        UserPermission(name="user_delete").save()
        print(f" - User Permissions OK")
