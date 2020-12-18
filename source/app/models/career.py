
from app.db import db


class Career(db.Model):

    id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column("name", db.String(64), nullable=False, unique=True)
    users = db.relationship("CareerUser", back_populates="career")
    cathedras = db.relationship("Cathedra", back_populates="career")
    is_deleted = db.Column(db.Boolean, nullable=False, default=False)

    def get_cathedras(self):
        return self.cathedras.select(lambda each: not each.is_deleted)

    def set_cathedras(self, cathedras):
        self.cathedras = self.cathedras.select(
            lambda each: each.is_deleted) + cathedras

    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()

    def update(self, name):
        self.name = name
        self.save()

    def remove(self):
        if self.id:
            self.is_deleted = True
            self.save()

    @classmethod
    def delete(self, id):
        career = self.query.get(id)
        if career:
            career.remove()
            return career
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
        career = self.query.get(id)
        return career if career and career.is_deleted == False else None

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
