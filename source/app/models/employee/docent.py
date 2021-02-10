
from app.models import Employee


class Docent(Employee):
    __mapper_args__ = {
        'polymorphic_identity': 1
    }

    @staticmethod
    def get_label():
        """Return employee tag """
        return "Docente"

    def is_docent(self):
        """Return if the employee is docent """
        return True
