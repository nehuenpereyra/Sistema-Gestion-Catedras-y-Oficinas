
from app.models import Employee


class NotDocent(Employee):
    __mapper_args__ = {
        'polymorphic_identity': 2
    }

    @staticmethod
    def get_label():
        """Return employee tag """
        return "No Docente"

    def is_not_docent(self):
        """Return if the employee is not docent """
        return True
