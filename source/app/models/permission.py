
from app.db import db
 
from .database_links import link_role_permission


class Permission(db.Model):

    id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column("name", db.String(32), nullable=False, unique=True)
    roles = db.relationship("Role", back_populates="permissions", secondary=link_role_permission)
    is_deleted = db.Column(db.Boolean, nullable=False, default=False)

    def get_roles(self):
        return self.roles.select(lambda each: not each.is_deleted)

    def set_roles(self, roles):
        self.roles = self.roles.select(
            lambda each: each.is_deleted) + roles

    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()

    def update(self, name, roles):
        self.name = name
        self.set_roles(roles)
        self.save()

    def remove(self):
        if self.id:
            self.is_deleted = True
            self.save()

    @classmethod
    def delete(self, id):
        permission = self.query.get(id)
        if permission:
            permission.remove()
            return permission
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
        permission = self.query.get(id)
        return permission if permission and permission.is_deleted==False else None
        

    @classmethod
    def get_all(self, ids):
        if not ids:
            return []
        query = self.query
        query = query.filter_by(is_deleted=False)
        return query.filter(self.id.in_(ids)).all()

 