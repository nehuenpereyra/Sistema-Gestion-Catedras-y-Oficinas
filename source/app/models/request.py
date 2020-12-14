
from app.db import db
 


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

    @staticmethod
    def delete(id):
        request = Request.query.get(id)
        if request:
            request.remove()
            return request
        return None

    @staticmethod
    def all():
        query = Request.query
        query = query.filter_by(is_deleted=False)
        query = query.order_by(Request.content.asc())
        return query.all()

    @staticmethod
    def all_paginated(page, per_page, ids=None):
        query = Request.query
        query = query.filter_by(is_deleted=False)
        query = query.order_by(Request.content.asc())
        if ids:
            query = query.filter(Request.id.in_(ids))
        return query.paginate(page=page, per_page=per_page, error_out=False)

    @staticmethod
    def get(id):
        request = Request.query.get(id)
        return request if request and request.is_deleted==False else None
        

    @staticmethod
    def get_all(ids):
        if not ids:
            return []
        query = Request.query
        query = query.filter_by(is_deleted=False)
        return query.filter(Request.id.in_(ids)).all()

    @staticmethod
    def find_by_is_resolved(is_resolved):
        query = Request.query.order_by(Request.content.asc())
        return query.filter_by(is_resolved=is_resolved, is_deleted=False)

    @staticmethod
    def find_by_timestamp(timestamp):
        query = Request.query.order_by(Request.content.asc())
        return query.filter_by(timestamp=timestamp, is_deleted=False)

 