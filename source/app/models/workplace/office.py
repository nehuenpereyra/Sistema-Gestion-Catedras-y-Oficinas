from app.db import db
from .workplace import Workplace 

class Office( Workplace):

    id = db.Column("id", db.Integer, db.ForeignKey('workplace.id'), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': 2
    }
