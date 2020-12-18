
from datetime import datetime

from app.db import db
from app.models import EmployeeReview


class JobPosition(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    start_date = db.Column(db.DateTime, default=datetime.now,
                           nullable=False, unique=False)
    end_date = db.Column(db.DateTime,
                         nullable=True, unique=False)
    charge = db.relationship(
        "Charge", back_populates="job_positions", uselist=False)
    charge_id = db.Column(db.Integer, db.ForeignKey(
        "charge.id"), nullable=False, unique=False)
    workplace = db.relationship(
        "Workplace", back_populates="staff", uselist=False)
    workplace_id = db.Column(db.Integer, db.ForeignKey(
        "workplace.id"), nullable=False, unique=False)
    employee = db.relationship(
        "Employee", back_populates="job_positions", uselist=False)
    employee_id = db.Column(db.Integer, db.ForeignKey(
        "employee.id"), nullable=False, unique=False)

    current_review = db.relationship(
        "EmployeeReview", back_populates="current_position", foreign_keys="EmployeeReview.current_position_id", uselist=False)
    old_review = db.relationship(
        "EmployeeReview", back_populates="old_position", foreign_keys="EmployeeReview.old_position_id", uselist=False)

    is_deleted = db.Column(db.Boolean, nullable=False, default=False)

    def __init__(self, review=True, **kwargs):
        super(JobPosition, self).__init__(**kwargs)

        if review:
            EmployeeReview.creation_type(self)

    def reassign(self, charge):
        self.finish(review=False)

        new_job_position = JobPosition(charge=charge, workplace=self.workplace,
                                       employee=self.employee, review=False)
        EmployeeReview.upgrade_type(new_job_position, self)

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

    def isActive(self):
        return True if self.end_date is None else False

    def finish(self, review=True):
        self.end_date = datetime.today()

        if review:
            EmployeeReview.elimination_type(self)

        self.save()

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
        return job_position if job_position and job_position.is_deleted == False else None

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

    def __lt__(self, other):
        return self.charge.order < other.charge.order
