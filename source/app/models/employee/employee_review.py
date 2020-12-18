
from datetime import datetime

from sqlalchemy import DateTime, cast

from app.db import db


class EmployeeReview(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.now,
                          nullable=False, unique=False)
    type = db.Column(db.Integer, nullable=False, unique=False)

    current_position_id = db.Column(db.Integer, db.ForeignKey(
        "job_position.id"), nullable=True, unique=False)
    current_position = db.relationship(
        "JobPosition", back_populates="current_review", foreign_keys=current_position_id, uselist=False)

    old_position_id = db.Column(db.Integer, db.ForeignKey(
        "job_position.id"), nullable=True, unique=False)
    old_position = db.relationship(
        "JobPosition", back_populates="old_review", foreign_keys=old_position_id, uselist=False)

    def is_creation_type(self):
        return self.type == 1

    def is_upgrade_type(self):
        return self.type == 2

    def is_elimination_type(self):
        return self.type == 3

    def get_employee(self):
        if not self.is_elimination_type():
            return self.current_position.employee
        else:
            return self.old_position.employee

    def get_workplace(self):
        if not self.is_elimination_type():
            return self.current_position.workplace
        else:
            return self.old_position.workplace

    def get_current_charge(self):
        return self.current_position.charge

    def get_old_charge(self):
        return self.old_position.charge

    def see(self):
        self.remove()

    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()

    def remove(self):
        if self.id:
            db.session.delete(self)
            db.session.commit()

    @classmethod
    def creation_type(self, position):
        return self(type=1, current_position=position)

    @classmethod
    def upgrade_type(self, current_position, old_position):
        return self(type=2, current_position=current_position, old_position=old_position)

    @classmethod
    def elimination_type(self, position):
        return self(type=3, old_position=position)

    @classmethod
    def all(self):
        return self.query.order_by(cast(self.timestamp, DateTime).asc()).all()

    @classmethod
    def all_paginated(self, page, per_page, ids=None):
        query = self.query.order_by(cast(self.timestamp, DateTime).asc())
        if ids is not None:
            query = query.filter(self.id.in_(ids))
        return query.paginate(page=page, per_page=per_page, error_out=False)

    @classmethod
    def get(self, id):
        return self.query.get(id)

    @classmethod
    def get_all(self, ids):
        if not ids:
            return []
        query = self.query
        return query.filter(self.id.in_(ids)).all()
