from flask_seeder import Seeder

from app.models import Cathedra, Career


class CathedraSeeder(Seeder):

    def __init__(self, db=None):
        super().__init__(db=db)
        self.priority = 2

    def run(self):
        print("[CathedraSeeder]")
        medicina = Career.find_by_name("Medicina").first()
        obstetricia = Career.find_by_name("Licenciatura en Obstetricia").first()
        [
            Cathedra(name="Anatomía", email="anatomia@med.unlp.edu.ar",phone="+54 2944 106568", location="Facultad de medicina", attention_time="9:00Hs a 20:00Hs", career=medicina),
            Cathedra(name="Biología", email="biologia@med.unlp.edu.ar",phone="+54 2944 106568", location="Facultad de medicina", attention_time="9:00Hs a 20:00Hs", career=medicina),
            Cathedra(name="Psicología", email="psicologia@med.unlp.edu.ar",phone="+54 2944 106568", location="Facultad de medicina", attention_time="9:00Hs a 20:00Hs", career=obstetricia),
            Cathedra(name="Epidemiología", email="epidemiologia@med.unlp.edu.ar",phone="+54 2944 106568", location="Facultad de medicina", attention_time="9:00Hs a 20:00Hs", career=obstetricia),
        ].do(lambda each: self.save(each))

    def save(self, cathedra):
        cathedra.save()
        print(f" - {cathedra.name} cathedra OK")
