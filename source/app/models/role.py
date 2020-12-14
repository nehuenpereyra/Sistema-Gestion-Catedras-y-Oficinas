
from app.db import db
 
from .database_links import link_user_role, link_role_permission


class Role(db.Model):

    id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column("name", db.String(32), nullable=False, unique=True)
    users = db.relationship("User", back_populates="roles", secondary=link_user_role)
    permissions = db.relationship("Permission", back_populates="roles", secondary=link_role_permission)
    is_deleted = db.Column(db.Boolean, nullable=False, default=False)

    def get_users(self):
        return self.users.select(lambda each: not each.is_deleted)

    def set_users(self, users):
        self.users = self.users.select(
            lambda each: each.is_deleted) + users
    def get_permissions(self):
        return self.permissions.select(lambda each: not each.is_deleted)

    def set_permissions(self, permissions):
        self.permissions = self.permissions.select(
            lambda each: each.is_deleted) + permissions

    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()

    def update(self, name, permissions):
        self.name = name
        self.set_permissions(permissions)
        self.save()

    def remove(self):
        if self.id:
            self.is_deleted = True
            self.save()

    @staticmethod
    def delete(id):
        role = Role.query.get(id)
        if role:
            role.remove()
            return role
        return None

    @staticmethod
    def all():
        query = Role.query
        query = query.filter_by(is_deleted=False)
        query = query.order_by(Role.name.asc())
        return query.all()

    @staticmethod
    def all_paginated(page, per_page, ids=None):
        query = Role.query
        query = query.filter_by(is_deleted=False)
        query = query.order_by(Role.name.asc())
        if ids:
            query = query.filter(Role.id.in_(ids))
        return query.paginate(page=page, per_page=per_page, error_out=False)

    @staticmethod
    def get(id):
        role = Role.query.get(id)
        return role if role and role.is_deleted==False else None
        

    @staticmethod
    def get_all(ids):
        if not ids:
            return []
        query = Role.query
        query = query.filter_by(is_deleted=False)
        return query.filter(Role.id.in_(ids)).all()

 