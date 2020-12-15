
from app.db import db
 


class Cathedra(db.Model):

    id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column("name", db.String(64), nullable=False, unique=False)
    email = db.Column("email", db.String(64), nullable=False, unique=True)
    phone = db.Column("phone", db.String(32), nullable=False, unique=False)
    location = db.Column("location", db.String(64), nullable=False, unique=False)
    attention_time = db.Column("attention_time", db.String(64), nullable=False, unique=False)
    career = db.relationship("Career", back_populates="cathedras", uselist=False)
    career_id = db.Column("career_id", db.Integer, db.ForeignKey("career.id"), nullable=False, unique=False)
    staff = db.relationship("JobPosition", back_populates="cathedra")
    is_deleted = db.Column(db.Boolean, nullable=False, default=False)

    def get_staff(self):
        return self.staff.select(lambda each: not each.is_deleted)

    def set_staff(self, staff):
        self.staff = self.staff.select(
            lambda each: each.is_deleted) + staff

    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()

    def update(self, name, email, phone, location, attention_time, career):
        self.name = name
        self.email = email
        self.phone = phone
        self.location = location
        self.attention_time = attention_time
        self.career = career
        self.save()

    def remove(self):
        if self.id:
            self.is_deleted = True
            self.save()

    @classmethod
    def delete(self, id):
        cathedra = self.query.get(id)
        if cathedra:
            cathedra.remove()
            return cathedra
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
        if ids:
            query = query.filter(self.id.in_(ids))
        return query.paginate(page=page, per_page=per_page, error_out=False)

    @classmethod
    def get(self, id):
        cathedra = self.query.get(id)
        return cathedra if cathedra and cathedra.is_deleted==False else None
        

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

 