from flask_seeder import Seeder

from app.models import Charge


class ChargeSeeder(Seeder):

    def __init__(self, db=None):
        super().__init__(db=db)
        self.priority = 1

    def run(self):
        print("[ChargeSeeder]")
        [
            Charge(name="Jefe de Cátedra", is_docent=True, order=1),
            Charge(name="JTP", is_docent=True, order=2),
            Charge(name="Secretario", is_docent=False, order=1),
            Charge(name="Portero", is_docent=False, order=2),
        ].do(lambda each: self.save(each))

    def save(self, charge):
        charge.save()
        print(f" - {charge.name} charge OK")
