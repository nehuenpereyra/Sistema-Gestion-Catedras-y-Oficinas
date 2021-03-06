
from app.db import db


class Charge(db.Model):

    id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column("name", db.String(64), nullable=False, unique=True)
    is_docent = db.Column("is_docent", db.Boolean, nullable=True, unique=False)
    order = db.Column("order", db.Integer, nullable=False, unique=False)
    job_positions = db.relationship("JobPosition", back_populates="charge")
    is_deleted = db.Column(db.Boolean, nullable=False, default=False)

    def has_job_positions(self):
        return self.job_positions.any_satisfy(lambda each: each.is_active())

    def get_job_positions(self):
        return self.job_positions.select(lambda each: not each.is_deleted)

    def set_job_positions(self, job_positions):
        self.job_positions = self.job_positions.select(
            lambda each: each.is_deleted) + job_positions

    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()

    def update(self, name, is_docent, order):
        self.name = name
        self.is_docent = is_docent
        self.order = order
        self.save()

    def remove(self):
        if self.id:
            self.is_deleted = True
            self.save()

    @classmethod
    def delete(self, id):
        charge = self.query.get(id)
        if charge:
            charge.remove()
            return charge
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
        charge = self.query.get(id)
        return charge if charge and charge.is_deleted == False else None

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
    def find_by_is_docent(self, is_docent):
        query = self.query.order_by(self.name.asc())
        return query.filter_by(is_docent=is_docent, is_deleted=False).all()

    @classmethod
    def find_by_order(self, order):
        query = self.query.order_by(self.name.asc())
        return query.filter_by(order=order, is_deleted=False).all()

    @classmethod
    def search(self, name, charge_type, page, per_page):
        query = self.query
        query = query.filter_by(is_deleted=False)
        query = query.order_by(self.name.asc())
        if not name is None and name != "":
            query = query.filter(self.name.like(f"%{name}%"))

        if not charge_type is None and charge_type != 0:
            query = query.filter_by(
                is_docent=True if charge_type == 1 else False)

        return query.paginate(page=page, per_page=per_page, error_out=False)
