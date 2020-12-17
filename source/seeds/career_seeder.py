from flask_seeder import Seeder

from app.models import Career


class CareerSeeder(Seeder):

    def __init__(self, db=None):
        super().__init__(db=db)
        self.priority = 1

    def run(self):
        print("[CareerSeeder]")

        [
            Career(name="Enfermería Universitaria"),
            Career(name="Licenciatura en Nutrición"),
            Career(name="Licenciatura en Obstetricia"),
            Career(name="Medicina"),
            Career(name="Tecnicatura en Prácticas Cardiológicas")
        ].do(lambda each: self.save(each))

    def save(self, career):
        career.save()
        print(f" - {career.name} career OK")
