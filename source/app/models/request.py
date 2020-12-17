
from app.db import db
from sqlalchemy import DateTime, cast


class Request(db.Model):

    id = db.Column("id", db.Integer, primary_key=True)
    content = db.Column("content", db.String(200), nullable=False, unique=False)
    is_resolved = db.Column("is_resolved", db.Boolean, nullable=True, unique=False)
    receive_email = db.Column("receive_email", db.Boolean, nullable=True, unique=False)
    timestamp = db.Column("timestamp", db.DateTime, nullable=False, unique=False)
    user = db.relationship("User", back_populates="requests", uselist=False)
    user_id = db.Column("user_id", db.Integer, db.ForeignKey("user.id"), nullable=False, unique=False)
    request_type = db.relationship("RequestType", back_populates="requests", uselist=False)
    request_type_id = db.Column("request_type_id", db.Integer, db.ForeignKey("request_type.id"), nullable=False, unique=False)
    is_deleted = db.Column(db.Boolean, nullable=False, default=False)


    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()

    def update(self, content, is_resolved, receive_email, timestamp, user, request_type):
        self.content = content
        self.is_resolved = is_resolved
        self.receive_email = receive_email
        self.timestamp = timestamp
        self.user = user
        self.request_type = request_type
        self.save()

    def remove(self):
        if self.id:
            self.is_deleted = True
            self.save()

    @classmethod
    def delete(self, id):
        request = self.query.get(id)
        if request:
            request.remove()
            return request
        return None

    @classmethod
    def all(self):
        query = self.query
        query = query.filter_by(is_deleted=False)
        query = query.order_by(cast(Request.timestamp, DateTime).asc())
        return query.all()
    
    @classmethod
    def reverse_all(self):
        query = self.query
        query = query.filter_by(is_deleted=False)
        query = query.order_by(cast(Request.timestamp, DateTime).desc())
        return query.all()

    @classmethod
    def all_paginated(self, page, per_page, ids=None):
        query = self.query
        query = query.filter_by(is_resolved=False, is_deleted=False)
        query = query.order_by(cast(Request.timestamp, DateTime).asc())
        if ids:
            query = query.filter(self.id.in_(ids))
        return query.paginate(page=page, per_page=per_page, error_out=False)

    @classmethod
    def get(self, id):
        request = self.query.get(id)
        return request if request and request.is_deleted==False else None
        

    @classmethod
    def get_all(self, ids):
        if not ids:
            return []
        query = self.query
        query = query.filter_by(is_deleted=False)
        return query.filter(self.id.in_(ids)).all()

    @classmethod
    def find_by_is_resolved(self, is_resolved):
        query = self.query.order_by(self.content.asc())
        return query.filter_by(is_resolved=is_resolved, is_deleted=False).all()

    @classmethod
    def find_by_timestamp(self, timestamp):
        query = self.query.order_by(self.content.asc())
        return query.filter_by(timestamp=timestamp, is_deleted=False).all()

 