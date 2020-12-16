
from flask_seeder import Seeder

from app.models import Employee, PendingEmployee


class EmployeeSeeder(Seeder):

    def __init__(self, db=None):
        super().__init__(db=db)
        self.priority = 4

    def run(self):
        print("[PendingEmployeeSeeder]")

        [
            PendingEmployee(
                name="Hiro",
                surname="Nakamura",
                dni="20602804",
                institutional_email="hiro.nakamura@med.unlp.edu.ar",
                type=1
            ),
            PendingEmployee(
                name="Peter",
                surname="Petrelli",
                dni="48900202",
                institutional_email="peter.petrelli@med.unlp.edu.ar",
                secondary_email="peter.petrelli@gmail.com",
                type=3
            ),
            PendingEmployee(
                name="Max",
                surname="Pacman",
                dni="38204820",
                institutional_email="max.pacman@med.unlp.edu.ar",
                secondary_email="max.pacman@gmail.com",
                linked_employee=Employee.find_by_name("Pedro").first()
            ),
            PendingEmployee(
                name="Isaac",
                surname="Mendez",
                dni="30200500",
                institutional_email="isaac.mendez@med.unlp.edu.ar",
                secondary_email="isaac.mendez@gmail.com",
                linked_employee=Employee.find_by_name("Luis").first()
            )
        ].do(lambda each: self.save(each))

    def save(self, employee):
        employee.save()
        print(f" - {employee.name} {employee.surname} pending employee OK")

