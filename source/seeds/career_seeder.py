from flask_seeder import Seeder

from app.models import Career


class CareerSeeder(Seeder):

    def __init__(self, db=None):
        super().__init__(db=db)
        self.priority = 1

    def run(self):
        print("[CareerSeeder]")

        [
            Career(name="Licenciatura en Informática"),
            Career(name="Licenciatura en Sistemas"),
            Career(name="Ingeniería en Computación"),
            Career(name="Analista Programador Universitario")
        ].do(lambda each: self.save(each))

    def save(self, career):
        career.save()
        print(f" - {career.name} career OK")
