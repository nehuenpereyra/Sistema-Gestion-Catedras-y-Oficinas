
from app.models import Employee

class Administrative(Employee):
    __mapper_args__ = {
        'polymorphic_identity': 3
    }