
from app.models import Employee

class Docent(Employee):
    __mapper_args__ = {
        'polymorphic_identity': 1
    }