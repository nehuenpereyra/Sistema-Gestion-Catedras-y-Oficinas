import bisect
from app.db import db


class Workplace(db.Model):

    id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column("name", db.String(64), nullable=False, unique=False)
    email = db.Column("email", db.String(64), nullable=False, unique=True)
    phone = db.Column("phone", db.String(32), nullable=False, unique=False)
    location = db.Column("location", db.String(64),
                         nullable=False, unique=False)
    staff = db.relationship("JobPosition", back_populates="workplace")
    is_deleted = db.Column(db.Boolean, nullable=False, default=False)
    type = db.Column(db.Integer, nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': 0,
        'polymorphic_on': type
    }

    def all_staff(self):
        return self.staff.select(lambda each: each.isActive())

    def all_employees(self):
        return self.all_staff().collect(lambda each: each.employee)

    def all_docent(self):
        return self.staff.select(lambda each: each.isActive() and each.employee.get_label() == "Docente").collect(lambda each: each.employee)

    def all_not_docent(self):
        return self.staff.select(lambda each: each.isActive() and each.employee.get_label() == "No Docente").collect(lambda each: each.employee)

    def all_administrative(self):
        return self.staff.select(lambda each: each.isActive() and each.employee.get_label() == "Administrativo").collect(lambda each: each.employee)

    def is_cathedra(self):
        return False

    def is_office(self):
        return False

    def get_staff(self):
        return self.staff.select(lambda each: not each.is_deleted)

    def set_staff(self, staff):
        self.staff = self.staff.select(
            lambda each: each.is_deleted) + staff

    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()

    def update(self, name, email, phone, location):
        self.name = name
        self.email = email
        self.phone = phone
        self.location = location
        self.save()

    def remove(self):
        if self.id:
            self.is_deleted = True
            self.save()

    @classmethod
    def delete(self, id):
        workplace = self.query.get(id)
        if workplace:
            workplace.remove()
            return workplace
        return None

    @classmethod
    def all(self):
        query = self.query
        query = query.filter_by(is_deleted=False)
        query = query.order_by(self.name.asc())
        return query.all()

    @classmethod
    def all_paginated(self, page, per_page, ids=None, only_ids=True):

        query = self.query
        query = query.filter_by(is_deleted=False)
        query = query.order_by(self.name.asc())

        if ids is not None:
            if only_ids:
                query = query.filter(self.id.in_(ids))
            else:
                query = query.filter(~self.id.in_(ids))

        return query.paginate(page=page, per_page=per_page, error_out=False)

    @classmethod
    def get(self, id):
        workplace = self.query.get(id)
        return workplace if workplace and workplace.is_deleted == False else None

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
    def find_by_email(self, email):
        query = self.query.order_by(self.name.asc())
        return query.filter_by(email=email, is_deleted=False).all()

    @classmethod
    def find_by_phone(self, phone):
        query = self.query.order_by(self.name.asc())
        return query.filter_by(phone=phone, is_deleted=False).all()

    def sttaf_json(self):
        charge_employees = []
        staff = {}
        charges = {}
        for data in self.staff:
            if data.isActive():
                bisect.insort(charge_employees, data)
        for charge_employee in charge_employees:
            if not charge_employee.charge.name in charges:
                charges[charge_employee.charge.name] = []
            charges[charge_employee.charge.name].add(charge_employee)
        for key, values in charges.items():
            if not values.first().employee.get_label() in staff:
                staff[values.first().employee.get_label()] = {
                    key: charges[key]}
            else:
                staff[values.first().employee.get_label()].update(
                    {key: charges[key]})
        return staff
