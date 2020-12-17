from flask_seeder import Seeder

from app.models import Office

class OfficeSeeder(Seeder):

    def __init__(self, db=None):
        super().__init__(db=db)
        self.priority = 2

    def run(self):
        print("[OfficeSeeder]")
        [
            Office(name="Oficina 1", email="oficina1@med.unlp.edu.ar",phone="+54 2944 106568", location="Facultad de medicina"),
            Office(name="Oficina 2", email="oficina2@med.unlp.edu.ar",phone="+54 2944 106568", location="Facultad de medicina"),
            Office(name="Oficina 3", email="oficina3@med.unlp.edu.ar",phone="+54 2944 106568", location="Facultad de medicina"),
            Office(name="Oficina 4", email="oficina4@med.unlp.edu.ar",phone="+54 2944 106568", location="Facultad de medicina"),
        ].do(lambda each: self.save(each))

    def save(self, office):
        office.save()
        print(f" - {office.name} office OK")
