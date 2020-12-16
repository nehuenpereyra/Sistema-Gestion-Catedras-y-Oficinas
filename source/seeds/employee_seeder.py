
from flask_seeder import Seeder

from app.models import Docent, NotDocent, Administrative


class EmployeeSeeder(Seeder):

    def __init__(self, db=None):
        super().__init__(db=db)
        self.priority = 3

    def run(self):
        print("[EmployeeSeeder]")

        [
            Docent(
                name="Laura",
                surname="Gomez",
                dni="60708202",
                institutional_email="laura.gomez@med.unlp.edu.ar",
                secondary_email="laura_gomez@gmail.com"
            ),
            Docent(
                name="Luis",
                surname="Alvarez",
                dni="20506792",
                institutional_email="luis.alvarez@med.unlp.edu.ar",
                secondary_email="luis_alvarez@gmail.com"
            ),
            Docent(
                name="Pedro",
                surname="Toroto",
                dni="60202504",
                institutional_email="pedro.toroto@med.unlp.edu.ar",
                secondary_email=None
            ),
            NotDocent(
                name="Maria Elena",
                surname="Fernández",
                dni="10125643",
                institutional_email="maria.fernandez@med.unlp.edu.ar",
                secondary_email="maria_fernandez@gmail.com"
            ),
            NotDocent(
                name="Lisa",
                surname="Díaz",
                dni="68200404",
                institutional_email="lisa.diaz@med.unlp.edu.ar",
                secondary_email="lisa_diaz@gmail.com"
            ),
            Administrative(
                name="Lucas",
                surname="Martínez",
                dni="50508902",
                institutional_email="lucas.martinez@med.unlp.edu.ar",
                secondary_email="lucas_martinez@gmail.com"
            ),
            Administrative(
                name="Emanuel",
                surname="Sánchez",
                dni="90205708",
                institutional_email="emanuel.sanchez@med.unlp.edu.ar",
                secondary_email="emanuel_sanchez@gmail.com"
            )
        ].do(lambda each: self.save(each))

    def save(self, employee):
        employee.save()
        print(f" - {employee.name} {employee.surname} employee OK")

