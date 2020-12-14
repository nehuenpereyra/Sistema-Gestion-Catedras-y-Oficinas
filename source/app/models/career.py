
from app.db import db
 
from .database_links import link_career_cathedra


class Career(db.Model):

    id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column("name", db.String(64), nullable=False, unique=True)
    cathedras = db.relationship("Cathedra", back_populates="careers", secondary=link_career_cathedra)
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

    @staticmethod
    def delete(id):
        career = Career.query.get(id)
        if career:
            career.remove()
            return career
        return None

    @staticmethod
    def all():
        query = Career.query
        query = query.filter_by(is_deleted=False)
        query = query.order_by(Career.name.asc())
        return query.all()

    @staticmethod
    def all_paginated(page, per_page, ids=None):
        query = Career.query
        query = query.filter_by(is_deleted=False)
        query = query.order_by(Career.name.asc())
        if ids:
            query = query.filter(Career.id.in_(ids))
        return query.paginate(page=page, per_page=per_page, error_out=False)

    @staticmethod
    def get(id):
        career = Career.query.get(id)
        return career if career and career.is_deleted==False else None
        

    @staticmethod
    def get_all(ids):
        if not ids:
            return []
        query = Career.query
        query = query.filter_by(is_deleted=False)
        return query.filter(Career.id.in_(ids)).all()

    @staticmethod
    def find_by_name(name):
        query = Career.query.order_by(Career.name.asc())
        return query.filter_by(name=name, is_deleted=False)

 