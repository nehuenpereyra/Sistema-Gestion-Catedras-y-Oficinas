from app.db import db
from .user_state import UserState

class OfficeUser(UserState):
    
    id = db.Column("id", db.Integer, db.ForeignKey('user_state.id'), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': 3
    }