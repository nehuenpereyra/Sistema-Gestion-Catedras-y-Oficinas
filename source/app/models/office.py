
from app.db import db
 


class Office(db.Model):

    id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column("name", db.String(64), nullable=False, unique=False)
    email = db.Column("email", db.String(64), nullable=False, unique=True)
    phone = db.Column("phone", db.String(32), nullable=False, unique=False)
    location = db.Column("location", db.String(64), nullable=False, unique=False)
    is_deleted = db.Column(db.Boolean, nullable=False, default=False)


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

    @staticmethod
    def delete(id):
        office = Office.query.get(id)
        if office:
            office.remove()
            return office
        return None

    @staticmethod
    def all():
        query = Office.query
        query = query.filter_by(is_deleted=False)
        query = query.order_by(Office.name.asc())
        return query.all()

    @staticmethod
    def all_paginated(page, per_page, ids=None):
        query = Office.query
        query = query.filter_by(is_deleted=False)
        query = query.order_by(Office.name.asc())
        if ids:
            query = query.filter(Office.id.in_(ids))
        return query.paginate(page=page, per_page=per_page, error_out=False)

    @staticmethod
    def get(id):
        office = Office.query.get(id)
        return office if office and office.is_deleted==False else None
        

    @staticmethod
    def get_all(ids):
        if not ids:
            return []
        query = Office.query
        query = query.filter_by(is_deleted=False)
        return query.filter(Office.id.in_(ids)).all()

    @staticmethod
    def find_by_name(name):
        query = Office.query.order_by(Office.name.asc())
        return query.filter_by(name=name, is_deleted=False)

    @staticmethod
    def find_by_email(email):
        query = Office.query.order_by(Office.name.asc())
        return query.filter_by(email=email, is_deleted=False)

    @staticmethod
    def find_by_phone(phone):
        query = Office.query.order_by(Office.name.asc())
        return query.filter_by(phone=phone, is_deleted=False)

 