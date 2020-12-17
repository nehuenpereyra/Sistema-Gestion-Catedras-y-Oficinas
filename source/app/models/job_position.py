
from app.db import db
 


class JobPosition(db.Model):

    id = db.Column("id", db.Integer, primary_key=True)
    start_date = db.Column("start_date", db.DateTime, nullable=False, unique=False)
    end_date = db.Column("end_date", db.DateTime, nullable=True, unique=False)
    charge = db.relationship("Charge", back_populates="job_positions", uselist=False)
    charge_id = db.Column("charge_id", db.Integer, db.ForeignKey("charge.id"), nullable=False, unique=False)
    workplace = db.relationship("Workplace", back_populates="staff", uselist=False)
    workplace_id = db.Column("workplace_id", db.Integer, db.ForeignKey("workplace.id"), nullable=False, unique=False)
    employee = db.relationship("Employee", back_populates="job_positions", uselist=False)
    employee_id = db.Column("employee_id", db.Integer, db.ForeignKey("employee.id"), nullable=False, unique=False)
    is_deleted = db.Column(db.Boolean, nullable=False, default=False)


    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()

    def update(self, start_date, end_date, charge, workplace, employee):
        self.start_date = start_date
        self.end_date = end_date
        self.charge = charge
        self.workplace = workplace
        self.employee = employee
        self.save()

    def remove(self):
        if self.id:
            self.is_deleted = True
            self.save()
    
    def isActive(self):
        return True if self.end_date is None else False

    @classmethod
    def delete(self, id):
        job_position = self.query.get(id)
        if job_position:
            job_position.remove()
            return job_position
        return None

    @classmethod
    def all(self):
        query = self.query
        query = query.filter_by(is_deleted=False)
        query = query.order_by(self.start_date.asc())
        return query.all()

    @classmethod
    def all_paginated(self, page, per_page, ids=None):
        query = self.query
        query = query.filter_by(is_deleted=False)
        query = query.order_by(self.start_date.asc())
        if ids is not None:
            query = query.filter(self.id.in_(ids))
        return query.paginate(page=page, per_page=per_page, error_out=False)

    @classmethod
    def get(self, id):
        job_position = self.query.get(id)
        return job_position if job_position and job_position.is_deleted==False else None
        

    @classmethod
    def get_all(self, ids):
        if not ids:
            return []
        query = self.query
        query = query.filter_by(is_deleted=False)
        return query.filter(self.id.in_(ids)).all()

    @classmethod
    def find_by_start_date(self, start_date):
        query = self.query.order_by(self.start_date.asc())
        return query.filter_by(start_date=start_date, is_deleted=False).all()

    @classmethod
    def find_by_end_date(self, end_date):
        query = self.query.order_by(self.start_date.asc())
        return query.filter_by(end_date=end_date, is_deleted=False).all()

 