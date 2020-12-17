
from app.db import db

from app.models.database_links import link_user_cathedra
from .workplace import Workplace


class Cathedra(Workplace):

    id = db.Column("id", db.Integer, db.ForeignKey('workplace.id'), primary_key=True)
    attention_time = db.Column("attention_time", db.String(64), nullable=False, unique=False)
    users = db.relationship("CathedraUser", back_populates="cathedras", secondary=link_user_cathedra)
    career = db.relationship("Career", back_populates="cathedras", uselist=False)
    career_id = db.Column("career_id", db.Integer, db.ForeignKey("career.id"), nullable=False, unique=False)

    __mapper_args__ = {
        'polymorphic_identity': 1
    }

    def update(self, name, email, phone, location, attention_time, career):
        self.name = name
        self.email = email
        self.phone = phone
        self.location = location
        self.attention_time = attention_time
        self.career = career
        self.save()

    def is_cathedra(self):
        return True