
from app.db import db
 


class Employee(db.Model):

    id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column("name", db.String(32), nullable=False, unique=False)
    surname = db.Column("surname", db.String(32), nullable=False, unique=False)
    dni = db.Column("dni", db.String(16), nullable=True, unique=False)
    institutional_email = db.Column("institutional_email", db.String(64), nullable=False, unique=False)
    secondary_email = db.Column("secondary_email", db.String(64), nullable=True, unique=False)
    job_positions = db.relationship("JobPosition", back_populates="employee")
    is_deleted = db.Column(db.Boolean, nullable=False, default=False)

    def get_job_positions(self):
        return self.job_positions.select(lambda each: not each.is_deleted)

    def set_job_positions(self, job_positions):
        self.job_positions = self.job_positions.select(
            lambda each: each.is_deleted) + job_positions

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

    @staticmethod
    def delete(id):
        employee = Employee.query.get(id)
        if employee:
            employee.remove()
            return employee
        return None

    @staticmethod
    def all():
        query = Employee.query
        query = query.filter_by(is_deleted=False)
        query = query.order_by(Employee.name.asc())
        return query.all()

    @staticmethod
    def all_paginated(page, per_page, ids=None):
        query = Employee.query
        query = query.filter_by(is_deleted=False)
        query = query.order_by(Employee.name.asc())
        if ids:
            query = query.filter(Employee.id.in_(ids))
        return query.paginate(page=page, per_page=per_page, error_out=False)

    @staticmethod
    def get(id):
        employee = Employee.query.get(id)
        return employee if employee and employee.is_deleted==False else None
        

    @staticmethod
    def get_all(ids):
        if not ids:
            return []
        query = Employee.query
        query = query.filter_by(is_deleted=False)
        return query.filter(Employee.id.in_(ids)).all()

    @staticmethod
    def find_by_name(name):
        query = Employee.query.order_by(Employee.name.asc())
        return query.filter_by(name=name, is_deleted=False)

    @staticmethod
    def find_by_surname(surname):
        query = Employee.query.order_by(Employee.name.asc())
        return query.filter_by(surname=surname, is_deleted=False)

    @staticmethod
    def find_by_dni(dni):
        query = Employee.query.order_by(Employee.name.asc())
        return query.filter_by(dni=dni, is_deleted=False)

    @staticmethod
    def find_by_institutional_email(institutional_email):
        query = Employee.query.order_by(Employee.name.asc())
        return query.filter_by(institutional_email=institutional_email, is_deleted=False)

    @staticmethod
    def find_by_secondary_email(secondary_email):
        query = Employee.query.order_by(Employee.name.asc())
        return query.filter_by(secondary_email=secondary_email, is_deleted=False)

 