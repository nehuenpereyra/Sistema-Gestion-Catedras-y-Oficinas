
from app.db import db

from app.models.database_links import link_user_office
from .workplace import Workplace 

class Office( Workplace):

    id = db.Column("id", db.Integer, db.ForeignKey('workplace.id'), primary_key=True)
    users = db.relationship("OfficeUser", back_populates="offices", secondary=link_user_office)

    __mapper_args__ = {
        'polymorphic_identity': 2
    }
