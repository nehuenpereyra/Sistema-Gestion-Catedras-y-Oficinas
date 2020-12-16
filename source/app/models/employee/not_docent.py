
from app.models import Employee

class NotDocent(Employee):
    __mapper_args__ = {
        'polymorphic_identity': 2
    }

    @staticmethod
    def get_label():
        return "No Docente"