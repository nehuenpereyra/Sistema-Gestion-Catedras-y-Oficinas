import re
from app.db import db


class Employee(db.Model):

    id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column("name", db.String(32), nullable=False, unique=False)
    surname = db.Column("surname", db.String(32), nullable=False, unique=False)
    dni = db.Column("dni", db.String(16), nullable=True, unique=True)
    institutional_email = db.Column(
        "institutional_email", db.String(64), nullable=False, unique=True)
    secondary_email = db.Column(
        "secondary_email", db.String(64), nullable=True, unique=True)
    job_positions = db.relationship("JobPosition", back_populates="employee")
    pending_changes = db.relationship(
        "PendingEmployee", back_populates="linked_employee")
    type = db.Column(db.Integer, nullable=False)
    is_deleted = db.Column(db.Boolean, nullable=False, default=False)

    __mapper_args__ = {
        'polymorphic_on': type,
        'polymorphic_identity': 0
    }

    @staticmethod
    def get_label():
        return "Empleado"

    def is_docent(self):
        return False

    def is_not_docent(self):
        return False

    def is_administrative(self):
        return False

    def has_charge(self, charges_ids, workplace):
        for job_position in workplace.all_staff():
            if job_position.employee == self:
                return charges_ids.any_satisfy(lambda each: each == job_position.charge.id)
        return False

    def check_fields(self, institutional_email, name, surname, secondary_email, dni):
        valid_institutional_email = True
        valid_name = True
        valid_surname = True
        valid_secondary_email = True
        valid_dni = True

        if not institutional_email is None:
            if self.institutional_email != institutional_email:
                valid_institutional_email = False

        if not name is None:
            if not bool(re.search(name.lower(), self.name.lower())):
                valid_name = False

        if not surname is None:
            if not bool(re.search(surname.lower(), self.surname.lower())):
                valid_surname = False

        if not secondary_email is None:
            if self.secondary_email != secondary_email:
                valid_secondary_email = False

        if not dni is None:
            if self.dni != dni:
                valid_dni = False

        return valid_institutional_email and valid_name and valid_surname and valid_secondary_email and valid_dni

    def get_job_positions(self):
        return self.job_positions.select(lambda each: not each.is_deleted)

    def set_job_positions(self, job_positions):
        self.job_positions = self.job_positions.select(
            lambda each: each.is_deleted) + job_positions

    def get_full_name(self):
        return f"{self.name} {self.surname}"

    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()

    def update(self, name, surname, dni, institutional_email, secondary_email):
        self.name = name
        self.surname = surname
        self.dni = dni
        self.institutional_email = institutional_email
        self.secondary_email = secondary_email
        self.save()

    def remove(self):
        if self.id:
            self.is_deleted = True
            self.save()

    @classmethod
    def delete(self, id):
        employee = self.query.get(id)
        if employee:
            employee.remove()
            return employee
        return None

    @classmethod
    def all(self):
        query = self.query
        query = query.filter_by(is_deleted=False)
        query = query.order_by(self.name.asc())
        return query.all()

    @classmethod
    def all_paginated(self, page, per_page, ids=None):
        query = self.query
        query = query.filter_by(is_deleted=False)
        query = query.order_by(self.name.asc())
        if ids is not None:
            query = query.filter(self.id.in_(ids))
        return query.paginate(page=page, per_page=per_page, error_out=False)

    @classmethod
    def get(self, id):
        employee = self.query.get(id)
        return employee if employee and employee.is_deleted == False else None

    @classmethod
    def get_all(self, ids):
        if not ids:
            return []
        query = self.query
        query = query.filter_by(is_deleted=False)
        return query.filter(self.id.in_(ids)).all()

    @classmethod
    def find_by_name(self, name):
        query = self.query.order_by(self.name.asc())
        return query.filter_by(name=name, is_deleted=False).all()

    @classmethod
    def find_by_surname(self, surname):
        query = self.query.order_by(self.name.asc())
        return query.filter_by(surname=surname, is_deleted=False).all()

    @classmethod
    def find_by_dni(self, dni):
        query = self.query.order_by(self.name.asc())
        return query.filter_by(dni=dni, is_deleted=False).all()

    @classmethod
    def find_by_institutional_email(self, institutional_email):
        query = self.query.order_by(self.name.asc())
        return query.filter_by(institutional_email=institutional_email, is_deleted=False).all()

    @classmethod
    def find_by_secondary_email(self, secondary_email):
        query = self.query.order_by(self.name.asc())
        return query.filter_by(secondary_email=secondary_email, is_deleted=False).all()
