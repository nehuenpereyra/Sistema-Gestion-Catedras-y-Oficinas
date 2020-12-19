
from app.models import Employee


class Administrative(Employee):
    __mapper_args__ = {
        'polymorphic_identity': 3
    }

    @staticmethod
    def get_label():
        return "Administrativo"

    def is_administrative(self):
        return True
