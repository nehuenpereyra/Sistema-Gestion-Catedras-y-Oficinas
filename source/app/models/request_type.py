
from app.db import db


class RequestType(db.Model):

    id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column("name", db.String(32), nullable=False, unique=True)
    message = db.Column("message", db.String(
        200), nullable=False, unique=False)
    state = db.Column("state", db.Boolean, nullable=True, unique=False)
    requests = db.relationship("Request", back_populates="request_type")
    is_deleted = db.Column(db.Boolean, nullable=False, default=False)

    def get_requests(self):
        return self.requests.select(lambda each: not each.is_deleted)

    def set_requests(self, requests):
        self.requests = self.requests.select(
            lambda each: each.is_deleted) + requests

    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()

    def update(self, name, message, state):
        self.name = name
        self.message = message
        self.state = state
        self.save()

    def remove(self):
        if self.id:
            self.is_deleted = True
            self.save()

    @classmethod
    def delete(self, id):
        request_type = self.query.get(id)
        if request_type:
            request_type.remove()
            return request_type
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
        query = query.filter(self.id.notin_([1]))
        query = query.order_by(self.name.asc())
        if ids is not None:
            query = query.filter(self.id.in_(ids))
        return query.paginate(page=page, per_page=per_page, error_out=False)

    @classmethod
    def get(self, id):
        request_type = self.query.get(id)
        return request_type if request_type and request_type.is_deleted == False else None

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
    def find_by_state(self, state):
        query = self.query.order_by(self.name.asc())
        return query.filter_by(state=state, is_deleted=False).all()
