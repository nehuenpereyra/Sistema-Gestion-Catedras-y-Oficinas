
from app.db import db
 


class Charge(db.Model):

    id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column("name", db.String(64), nullable=False, unique=True)
    is_docent = db.Column("is_docent", db.Boolean, nullable=True, unique=False)
    order = db.Column("order", db.Integer, nullable=False, unique=False)
    job_positions = db.relationship("JobPosition", back_populates="charge")
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

    def update(self, name, is_docent, order):
        self.name = name
        self.is_docent = is_docent
        self.order = order
        self.save()

    def remove(self):
        if self.id:
            self.is_deleted = True
            self.save()

    @staticmethod
    def delete(id):
        charge = Charge.query.get(id)
        if charge:
            charge.remove()
            return charge
        return None

    @staticmethod
    def all():
        query = Charge.query
        query = query.filter_by(is_deleted=False)
        query = query.order_by(Charge.name.asc())
        return query.all()

    @staticmethod
    def all_paginated(page, per_page, ids=None):
        query = Charge.query
        query = query.filter_by(is_deleted=False)
        query = query.order_by(Charge.name.asc())
        if ids:
            query = query.filter(Charge.id.in_(ids))
        return query.paginate(page=page, per_page=per_page, error_out=False)

    @staticmethod
    def get(id):
        charge = Charge.query.get(id)
        return charge if charge and charge.is_deleted==False else None
        

    @staticmethod
    def get_all(ids):
        if not ids:
            return []
        query = Charge.query
        query = query.filter_by(is_deleted=False)
        return query.filter(Charge.id.in_(ids)).all()

    @staticmethod
    def find_by_name(name):
        query = Charge.query.order_by(Charge.name.asc())
        return query.filter_by(name=name, is_deleted=False)

    @staticmethod
    def find_by_is_docent(is_docent):
        query = Charge.query.order_by(Charge.name.asc())
        return query.filter_by(is_docent=is_docent, is_deleted=False)

    @staticmethod
    def find_by_order(order):
        query = Charge.query.order_by(Charge.name.asc())
        return query.filter_by(order=order, is_deleted=False)

 