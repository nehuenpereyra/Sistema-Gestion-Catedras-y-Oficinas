import re
from app.db import db
from sqlalchemy import func


class Employee(db.Model):

    id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column("name", db.String(32), nullable=False, unique=False)
    surname = db.Column("surname", db.String(32), nullable=False, unique=False)
    dni = db.Column("dni", db.String(16), nullable=True, unique=True)
    institutional_email = db.Column(
        "institutional_email", db.String(64), nullable=False, unique=True)
    secondary_email = db.Column(
        "secondary_email", db.String(64), nullable=True, unique=True)
    job_positions = db.relationship("JobPosition", back_populates="employee")
    pending_changes = db.relationship(
        "PendingEmployee", back_populates="linked_employee")
    type = db.Column(db.Integer, nullable=False)
    is_deleted = db.Column(db.Boolean, nullable=False, default=False)

    __mapper_args__ = {
        'polymorphic_on': type,
        'polymorphic_identity': 0
    }

    @staticmethod
    def get_label():
        """Return employee label """
        return "Empleado"

    def is_docent(self):
        """Return if the employee is docent """
        return False

    def is_not_docent(self):
        """Return if the employee is not docent """
        return False

    def is_administrative(self):
        """Return if the employee is administrative """
        return False

    def has_charge(self, charges_ids, workplace):
        """Determine if the employee is assigned some of the charges sent by parameters

        Parameters:
        charges_ids (list): list of charge ids
        workplace (class): workplace object

        Returns:
        boolean:Returns true if you have any of the charges

        """
        for job_position in workplace.all_staff():
            if job_position.employee == self:
                return charges_ids.any_satisfy(lambda each: each == job_position.charge.id)
        return False

    def has_active_charge(self):
        return self.job_positions.any_satisfy(lambda each: each.is_active())

    def check_fields(self, institutional_email, name, surname, secondary_email, dni):
        """Validate the fields sent by parameter

        Parameters:
        institutional_email (string): institutional_email of the employee
        name (string): name of the employee
        surname (string): surname of the employee
        secondary_email (string): secondary_email of the employee
        dni (string): dni of the employee

        Returns:
        boolean:Returns true if the fields are valid

        """
        valid_institutional_email = True
        valid_name = True
        valid_surname = True
        valid_secondary_email = True
        valid_dni = True

        if not institutional_email is None:
            if self.institutional_email != institutional_email:
                valid_institutional_email = False

        if not name is None:
            if not bool(re.search(name.lower(), self.name.lower())):
                valid_name = False

        if not surname is None:
            if not bool(re.search(surname.lower(), self.surname.lower())):
                valid_surname = False

        if not secondary_email is None:
            if self.secondary_email != secondary_email:
                valid_secondary_email = False

        if not dni is None:
            if self.dni != dni:
                valid_dni = False

        return valid_institutional_email and valid_name and valid_surname and valid_secondary_email and valid_dni

    def get_job_positions(self):
        """Returns current employee job positions """
        return self.job_positions.select(lambda each: not each.is_deleted)

    def set_job_positions(self, job_positions):
        """Set a job position for the employee

        Parameters:
        job_positions (object): institutional_email of the employee

        """
        self.job_positions = self.job_positions.select(
            lambda each: each.is_deleted) + job_positions

    def get_full_name(self):
        """Returns full name of employee """
        return f"{self.name} {self.surname}"

    def save(self):
        """Save the employee in the database """
        if not self.id:
            db.session.add(self)
        db.session.commit()

    def update(self, name, surname, dni, institutional_email, secondary_email):
        """Updates the employee attributes

        Parameters:
        institutional_email (string): institutional_email of the employee
        name (string): name of the employee
        surname (string): surname of the employee
        secondary_email (string): secondary_email of the employee
        dni (string): dni of the employee

        """
        self.name = name
        self.surname = surname
        self.dni = dni
        self.institutional_email = institutional_email
        self.secondary_email = secondary_email
        self.save()

    def remove(self):
        """Logically delete the employee"""
        if self.id:
            self.pending_changes.do(lambda each: each.remove())

            self.is_deleted = True
            self.save()

    @classmethod
    def delete(self, id):
        """Logically delete an employee using the employee's id 

        Parameters:
        id (int): employee id

        Returns:
        employee:Returns the employee if it is eliminated but None

        """
        employee = self.query.get(id)
        if employee:
            employee.remove()
            return employee
        return None

    @classmethod
    def all(self):
        """Returns all active employees and sorted by name in ascending order """
        query = self.query
        query = query.filter_by(is_deleted=False)
        query = query.order_by(self.name.asc())
        return query.all()

    @classmethod
    def all_paginated(self, page, per_page, ids=None):
        """Returns all paged active employees 

        Parameters:
        page (int): actual page
        per_page (int): number of employees per page
        ids (list): list of employee ids to which you have access permission

        Returns:
        object:Returns a object of paginated employees

        """
        query = self.query
        query = query.filter_by(is_deleted=False)
        query = query.order_by(self.name.asc())
        if ids is not None:
            query = query.filter(self.id.in_(ids))
        return query.paginate(page=page, per_page=per_page, error_out=False)

    @classmethod
    def get(self, id):
        """Returns the employee with the id passed by parameter """
        employee = self.query.get(id)
        return employee if employee and employee.is_deleted == False else None

    @classmethod
    def get_all(self, ids):
        """Returns all active employees 

        Parameters:
        ids (list): list of employee ids to which you have access permission

        Returns:
        list:Returns a list of employees

        """
        if not ids:
            return []
        query = self.query
        query = query.filter_by(is_deleted=False)
        return query.filter(self.id.in_(ids)).all()

    @classmethod
    def find_by_name(self, name):
        """Search for active employees by name  

        Parameters:
        name (string): name of the employee

        Returns:
        employee:Returns a employee or None

        """
        query = self.query.order_by(self.name.asc())
        return query.filter_by(name=name, is_deleted=False).all()

    @classmethod
    def find_by_surname(self, surname):
        """Search for active employees by surname  

        Parameters:
        surname (string): surname of the employee

        Returns:
        employee:Returns a employee or None

        """
        query = self.query.order_by(self.name.asc())
        return query.filter_by(surname=surname, is_deleted=False).all()

    @classmethod
    def find_by_dni(self, dni):
        """Search for active employees by dni  

        Parameters:
        dni (string): dni of the employee

        Returns:
        employee:Returns a employee or None

        """
        query = self.query.order_by(self.name.asc())
        return query.filter_by(dni=dni, is_deleted=False).all()

    @classmethod
    def find_by_institutional_email(self, institutional_email):
        """Search for active employees by institutional email  

        Parameters:
        institutional email (string): institutional email of the employee

        Returns:
        employee:Returns a employee or None

        """
        query = self.query.order_by(self.name.asc())
        return query.filter_by(institutional_email=institutional_email, is_deleted=False).all()

    @classmethod
    def find_by_secondary_email(self, secondary_email):
        """Search for active employees by secondary email  

        Parameters:
        secondary email (string): secondary email of the employee

        Returns:
        employee:Returns a employee or None

        """
        query = self.query.order_by(self.name.asc())
        return query.filter_by(secondary_email=secondary_email, is_deleted=False).all()

    @classmethod
    def search(self, employee_attributes, employee_charge_id, employee_type_ids, search_text, page, per_page):
        """Returns a paginated list of employees that meet the search criteria   

        Parameters:
        employee_attributes (int): number that identifies the search by name (0) and the search by surname (1) 
        employee_charge_id (int): employee charge id
        employee_type_ids (int): id of the type of employee (docent, not docent or administrative)
        page (int): actual page
        per_page (int): number of employees per page

        Returns:
        object:Returns a paginated object with the employees that meet the search criteria

        """
        query = self.query
        query = query.filter_by(is_deleted=False)
        query = query.order_by(self.name.asc())
        if not search_text is None and search_text != "" and not employee_attributes is None:
            if employee_attributes == 0:
                query = query.filter(func.concat(
                    Employee.name, ' ', Employee.surname).like(f"%{search_text}%"))
            if employee_attributes == 1:
                query = query.filter(self.name.like(f"%{search_text}%"))
            if employee_attributes == 2:
                query = query.filter(self.surname.like(f"%{search_text}%"))

        if not employee_type_ids is None and employee_type_ids != 0:
            if employee_type_ids == 1:
                query = query.filter(self.type == 1)
            if employee_type_ids == 2:
                query = query.filter(self.type == 2)
            if employee_type_ids == 3:
                query = query.filter(self.type == 3)

        if not employee_charge_id is None and employee_charge_id != 0:
            query = query.filter(self.job_positions.any(
                charge_id=employee_charge_id))

        return query.paginate(page=page, per_page=per_page, error_out=False)
