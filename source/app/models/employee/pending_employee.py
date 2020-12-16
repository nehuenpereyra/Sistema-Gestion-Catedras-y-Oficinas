
from datetime import datetime

from sqlalchemy import DateTime, cast

from app.db import db
from app.models import Docent, NotDocent, Administrative


class PendingEmployee(db.Model):

    id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column("name", db.String(32), nullable=False, unique=False)
    surname = db.Column("surname", db.String(32), nullable=False, unique=False)
    dni = db.Column("dni", db.String(16), nullable=True, unique=False)
    institutional_email = db.Column("institutional_email", db.String(64), nullable=False, unique=False)
    secondary_email = db.Column("secondary_email", db.String(64), nullable=True, unique=False)
    timestamp = db.Column(db.DateTime, default=datetime.now, nullable=False, unique=False)
    type = db.Column(db.Integer, nullable=True, unique=False)
    linked_employee_id = db.Column(db.Integer, db.ForeignKey("employee.id"), nullable=True, unique=False)
    linked_employee = db.relationship("Employee", back_populates="pending_changes", uselist=False)


    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()

    def remove(self):
        if self.id:
            db.session.delete(self)
            db.session.commit()

    @classmethod
    def all(self):
        return self.query.order_by(cast(self.timestamp, DateTime).asc()).all()

    @classmethod
    def all_paginated(self, page, per_page, ids=None):
        query = self.query.order_by(cast(self.timestamp, DateTime).asc())
        if ids:
            query = query.filter(self.id.in_(ids))
        return query.paginate(page=page, per_page=per_page, error_out=False)

    @classmethod
    def get(self, id):
        employee = self.query.get(id)
        return employee if employee and employee.is_deleted==False else None
        
    @classmethod
    def get_all(self, ids):
        if not ids:
            return []
        query = self.query
        return query.filter(self.id.in_(ids)).all()

    def is_new(self):
        return self.linked_employee is None

    def get_employee_class(self):
        employee_class = {
            1: Docent,
            2: NotDocent,
            3: Administrative
        }

        return employee_class[self.type]

    def accept(self):
        if self.is_new():
            self.get_employee_class()(
                name = self.name,
                surname = self.surname,
                dni = self.dni,
                institutional_email = self.institutional_email,
                secondary_email = self.secondary_email
            ).save()
        else:
            self.linked_employee.update(
                name = self.name,
                surname = self.surname,
                dni = self.dni,
                institutional_email = self.institutional_email,
                secondary_email = self.secondary_email
            )

        self.remove()
    
    def reject(self):
        self.remove()