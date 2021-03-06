
from flask_seeder import Seeder

from app.models import Permission


class PermissionSeeder(Seeder):

    def __init__(self, db=None):
        super().__init__(db=db)
        self.priority = 1

    def run(self):
        print("[PermissionSeeder]")

        Permission(name="configuration_update").save()
        print(f" - Configuration Permission OK")

        Permission(name="user_index").save()
        Permission(name="user_show").save()
        Permission(name="user_create").save()
        Permission(name="user_update").save()
        Permission(name="user_delete").save()
        print(f" - User Permissions OK")

        Permission(name="career_index").save()
        Permission(name="career_show").save()
        Permission(name="career_create").save()
        Permission(name="career_update").save()
        Permission(name="career_delete").save()
        print(f" - Career Permissions OK")

        Permission(name="cathedra_index").save()
        Permission(name="cathedra_show").save()
        Permission(name="cathedra_create").save()
        Permission(name="cathedra_update").save()
        Permission(name="cathedra_delete").save()
        print(f" - Cathedra Permissions OK")

        Permission(name="office_index").save()
        Permission(name="office_show").save()
        Permission(name="office_create").save()
        Permission(name="office_update").save()
        Permission(name="office_delete").save()
        print(f" - Office Permissions OK")

        Permission(name="charge_index").save()
        Permission(name="charge_show").save()
        Permission(name="charge_create").save()
        Permission(name="charge_update").save()
        Permission(name="charge_delete").save()
        print(f" - Charge Permissions OK")

        Permission(name="employee_index").save()
        Permission(name="employee_show").save()
        Permission(name="employee_create").save()
        Permission(name="employee_update").save()
        Permission(name="employee_delete").save()
        print(f" - Employee Permissions OK")

        Permission(name="job_position_index").save()
        Permission(name="job_position_show").save()
        Permission(name="job_position_create").save()
        Permission(name="job_position_update").save()
        Permission(name="job_position_delete").save()
        print(f" - Job Position Permissions OK")

        Permission(name="request_index").save()
        Permission(name="request_show").save()
        Permission(name="request_create").save()
        Permission(name="request_update").save()
        Permission(name="request_delete").save()
        print(f" - Request Permissions OK")

        Permission(name="request_type_index").save()
        Permission(name="request_type_show").save()
        Permission(name="request_type_create").save()
        Permission(name="request_type_update").save()
        Permission(name="request_type_delete").save()
        print(f" - Request Type Permissions OK")

        Permission(name="pending_employee_index").save()
        Permission(name="pending_employee_show").save()
        Permission(name="pending_employee_accept").save()
        Permission(name="pending_employee_reject").save()
        print(f" - Pending Employee Permissions OK")

        Permission(name="employee_review_index").save()
        Permission(name="employee_review_see").save()

        Permission(name="user_content_index").save()
        Permission(name="user_content_assign").save()
        Permission(name="user_content_unassign").save()
        print(f" - User Content Permissions OK")

        Permission(name="cathedra_report").save()
        Permission(name="office_report").save()
        Permission(name="career_report").save()
        print(f" - Reports Permissions OK")
