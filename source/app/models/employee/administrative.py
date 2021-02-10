
from app.models import Employee


class Administrative(Employee):
    __mapper_args__ = {
        'polymorphic_identity': 3
    }

    @staticmethod
    def get_label():
        """Return employee tag """
        return "Administrativo"

    def is_administrative(self):
        """Return if the employee is administrative """
        return True
