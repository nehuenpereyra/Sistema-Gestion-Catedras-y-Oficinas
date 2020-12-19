import random
import string
from app.db import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app.models.database_links import link_user_role
from .career_user import CareerUser
from .cathedra_user import CathedraUser
from .office_user import OfficeUser


def get_permission_method(user, permission):

    permission_mapper = {
        "user": user.allowed_user_id_list,
        "role": user.allowed_role_id_list,
        "permission": user.allowed_permission_id_list,
        "request": user.allowed_request_id_list,
        "career": user.allowed_career_id_list,
        "cathedra": user.allowed_cathedra_id_list,
        "office": user.allowed_office_id_list,
        "charge": user.allowed_charge_id_list,
        "employee": user.allowed_employee_id_list,
        "job_position": user.allowed_job_position_id_list,
        "request_type": user.allowed_request_type_id_list
    }

    return permission_mapper[permission]


class User(UserMixin, db.Model):

    __tablename__ = "user"

    id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column("name", db.String(32), nullable=False, unique=False)
    surname = db.Column("surname", db.String(32), nullable=False, unique=False)
    username = db.Column("username", db.String(32),
                         nullable=False, unique=False)
    password = db.Column("password", db.String(128),
                         nullable=False, unique=False)
    institutional_email = db.Column(
        "institutional_email", db.String(64), nullable=False, unique=False)
    secondary_email = db.Column(
        "secondary_email", db.String(64), nullable=False, unique=False)
    roles = db.relationship(
        "Role", back_populates="users", secondary=link_user_role)
    requests = db.relationship("Request", back_populates="user")
    is_deleted = db.Column(db.Boolean, nullable=False, default=False)
    state = db.relationship(
        "UserState", back_populates="user", uselist=False)
    recovery_link = db.Column(db.String(32), nullable=True, unique=False)

    def is_career_manager(self):
        return self.roles.any_satisfy(lambda each: each.name == "Responsable de Carrera")

    def is_cathedra_manager(self):
        return self.roles.any_satisfy(lambda each: each.name == "Responsable de Catedra")

    def is_office_manager(self):
        return self.roles.any_satisfy(lambda each: each.name == "Responsable de Oficina")

    def is_visitante(self):
        return self.roles.any_satisfy(lambda each: each.name == "Visitante")

    def get_career(self):
        return self.state.career

    def get_cathedras(self):
        return self.state.cathedras

    def get_offices(self):
        return self.state.offices

    def get_responsible_content_label(self):
        return self.state.get_responsible_content_label()

    def is_responsible(self):
        return self.state is not None

    def is_responsible_of_elements(self):
        return self.is_responsible() and self.state.is_responsible_of_elements()

    def add_responsible_element(self, element):
        self.state.add_responsible_element(element)

    def remove_responsible_element(self, element):
        self.state.remove_responsible_element(element)

    def get_roles(self):
        return self.roles.select(lambda each: not each.is_deleted)

    def get_responsible_role(self, roles):
        return roles.detect(lambda each: each.name == "Responsable de Catedra" or each.name ==
                            "Responsable de Oficina" or each.name == "Responsable de Carrera")

    def responsible_role_changed(self, roles):
        return self.get_responsible_role(self.roles) is not self.get_responsible_role(roles)

    def set_recovery_link(self):
        self.recovery_link = ''.join(
            (random.choice((string.ascii_letters + string.digits)) for i in range(32)))
        self.save()
        return self.recovery_link

    def remove_recovery_link(self):
        self.recovery_link = None
        self.save()

    def set_roles(self, roles):

        if self.responsible_role_changed(roles):
            if self.is_responsible():
                self.state.remove()

            responsible_role = self.get_responsible_role(roles)

            if responsible_role:
                if responsible_role.name == "Responsable de Carrera":
                    self.state = CareerUser()
                elif responsible_role.name == "Responsable de Catedra":
                    self.state = CathedraUser()
                elif responsible_role.name == "Responsable de Oficina":
                    self.state = OfficeUser()
            # else:
            #     self.state = None

        self.roles = roles

    def get_requests(self):
        return self.requests.select(lambda each: not each.is_deleted)

    def set_requests(self, requests):
        self.requests = self.requests.select(
            lambda each: each.is_deleted) + requests

    def get_full_name(self):
        return f"{self.name} {self.surname}"

    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()

    def update(self, name, surname, username, password, institutional_email, secondary_email, roles):
        self.name = name
        self.surname = surname
        self.username = username
        self.password = password
        self.institutional_email = institutional_email
        self.secondary_email = secondary_email
        self.set_roles(roles)
        self.save()

    def remove(self):
        if self.id:
            self.is_deleted = True
            self.save()

    @classmethod
    def delete(self, id):
        user = self.query.get(id)
        if user:
            user.remove()
            return user
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
        if ids is not None:
            query = query.filter(self.id.in_(ids))
        return query.paginate(page=page, per_page=per_page, error_out=False)

    @classmethod
    def get(self, id):
        user = self.query.get(id)
        return user if user and user.is_deleted == False else None

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
    def find_by_surname(self, surname):
        query = self.query.order_by(self.name.asc())
        return query.filter_by(surname=surname, is_deleted=False).all()

    @classmethod
    def find_by_recovery_link(self, recovery_link):
        return self.query.filter_by(recovery_link=recovery_link, is_deleted=False).first()

    @classmethod
    def find_by_username(self, username):
        query = self.query.order_by(self.name.asc())
        return query.filter_by(username=username, is_deleted=False).all()

    @classmethod
    def find_by_password(self, password):
        query = self.query.order_by(self.name.asc())
        return query.filter_by(password=password, is_deleted=False).all()

    @classmethod
    def find_by_institutional_email(self, institutional_email):
        query = self.query.order_by(self.name.asc())
        return query.filter_by(institutional_email=institutional_email, is_deleted=False).all()

    @classmethod
    def find_by_secondary_email(self, secondary_email):
        query = self.query.order_by(self.name.asc())
        return query.filter_by(secondary_email=secondary_email, is_deleted=False).all()

    def set_password(self, password):
        self.password = generate_password_hash(password)

    @staticmethod
    def login(username, password):
        user = User.query.filter_by(username=username).first()
        if user and (check_password_hash(user.password, password)):
            return user
        return None

    def is_admin(self):
        return self.roles.any_satisfy(lambda each: each.name == "Administrador")

    def has_permission_for(self, permission, id):
        has_permission = self.roles.flat_collect(lambda each: each.permissions). \
            any_satisfy(lambda each: each.name == permission)

        if not has_permission:
            return False
        elif not id or self.is_admin():
            return True

        allowed_id_list_method = get_permission_method(
            self, permission.split("_").first())

        allowed_id_list = allowed_id_list_method()

        if allowed_id_list is None:
            return True

        return allowed_id_list.includes(id)

    def allowed_user_id_list(self):
        return [self.id]

    def allowed_role_id_list(self):
        return []

    def allowed_permission_id_list(self):
        return []

    def allowed_request_id_list(self):
        return self.requests.collect(lambda each: each.id)

    def allowed_request_type_id_list(self):
        return []

    def allowed_career_id_list(self):
        if not self.state:
            return []

        return self.state.allowed_career_id_list()

    def allowed_cathedra_id_list(self):
        if not self.state:
            return []

        return self.state.allowed_cathedra_id_list()

    def allowed_office_id_list(self):
        if not self.state:
            return []

        return self.state.allowed_office_id_list()

    def allowed_charge_id_list(self):
        return []

    def allowed_employee_id_list(self):
        if not self.state:
            return []

        return self.state.allowed_employee_id_list()

    def allowed_job_position_id_list(self):
        if not self.state:
            return []

        return self.state.allowed_job_position_id_list()
