from flask_seeder import Seeder

from app.models import RequestType


class RequestTypeSeeder(Seeder):

    def __init__(self, db=None):
        super().__init__(db=db)
        self.priority = 1

    def run(self):
        print("[RequestTypeSeeder]")

        [
            RequestType(name="Consulta Técnica", message="", state=True),
            RequestType(name="Cartelera Virtual",
                        message="Descripción", state=True),
            RequestType(name="Email institucional",
                        message="Descripción", state=True)

        ].do(lambda each: self.save(each))

    def save(self, request_type):
        request_type.save()
        print(f" - {request_type.name} request_type OK")
