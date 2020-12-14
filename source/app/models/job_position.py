
from app.db import db
 


class JobPosition(db.Model):

    id = db.Column("id", db.Integer, primary_key=True)
    start_date = db.Column("start_date", db.DateTime, nullable=False, unique=False)
    end_date = db.Column("end_date", db.DateTime, nullable=True, unique=False)
    charge = db.relationship("Charge", back_populates="job_positions", uselist=False)
    charge_id = db.Column("charge_id", db.Integer, db.ForeignKey("charge.id"), nullable=False, unique=False)
    cathedra = db.relationship("Cathedra", back_populates="staff", uselist=False)
    cathedra_id = db.Column("cathedra_id", db.Integer, db.ForeignKey("cathedra.id"), nullable=False, unique=False)
    employee = db.relationship("Employee", back_populates="job_positions", uselist=False)
    employee_id = db.Column("employee_id", db.Integer, db.ForeignKey("employee.id"), nullable=False, unique=False)
    is_deleted = db.Column(db.Boolean, nullable=False, default=False)


    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()

    def update(self, start_date, end_date, charge, cathedra, employee):
        self.start_date = start_date
        self.end_date = end_date
        self.charge = charge
        self.cathedra = cathedra
        self.employee = employee
        self.save()

    def remove(self):
        if self.id:
            self.is_deleted = True
            self.save()

    @staticmethod
    def delete(id):
        job_position = JobPosition.query.get(id)
        if job_position:
            job_position.remove()
            return job_position
        return None

    @staticmethod
    def all():
        query = JobPosition.query
        query = query.filter_by(is_deleted=False)
        query = query.order_by(JobPosition.start_date.asc())
        return query.all()

    @staticmethod
    def all_paginated(page, per_page, ids=None):
        query = JobPosition.query
        query = query.filter_by(is_deleted=False)
        query = query.order_by(JobPosition.start_date.asc())
        if ids:
            query = query.filter(JobPosition.id.in_(ids))
        return query.paginate(page=page, per_page=per_page, error_out=False)

    @staticmethod
    def get(id):
        job_position = JobPosition.query.get(id)
        return job_position if job_position and job_position.is_deleted==False else None
        

    @staticmethod
    def get_all(ids):
        if not ids:
            return []
        query = JobPosition.query
        query = query.filter_by(is_deleted=False)
        return query.filter(JobPosition.id.in_(ids)).all()

    @staticmethod
    def find_by_start_date(start_date):
        query = JobPosition.query.order_by(JobPosition.start_date.asc())
        return query.filter_by(start_date=start_date, is_deleted=False)

    @staticmethod
    def find_by_end_date(end_date):
        query = JobPosition.query.order_by(JobPosition.start_date.asc())
        return query.filter_by(end_date=end_date, is_deleted=False)

 