from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

from app.db import db
from app.models.user_role import UserRole, link_user_role


class User(UserMixin, db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), nullable=False)
    surname = db.Column(db.String(32), nullable=False)
    email = db.Column(db.String(32), unique=True, nullable=False)
    username = db.Column(db.String(32), nullable=False)
    password = db.Column(db.String(128), nullable=False)
    roles = db.relationship(
        "UserRole", secondary=link_user_role, back_populates="users")
    is_active = db.Column(db.Boolean, nullable=False, default=True)

    def has_role(self, role):
        for each in self.roles:
            if each.name == role:
                return True
        return False

    @property
    def get_email(self):
        return self.email

    def set_email(self, value):
        self.email = value

    @property
    def get_name(self):
        return self.name

    @property
    def get_surname(self):
        return self.surname

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()

    def remove(self):
        if self.id:
            db.session.delete(self)
            db.session.commit()

    def __repr__(self):
        return f'<User {self.email}>'

    @staticmethod
    def update(id, name, surname, email, username, roles, is_active, password):
        user = User.query.get(id)
        if user:
            user.name = name
            user.surname = surname
            user.email = email
            user.username = username
            user.roles = roles
            user.is_active = is_active
            if password:
                user.set_password(password)
            user.save()
            return user
        return None

    @staticmethod
    def delete(id):
        user = User.query.get(id)
        if user:
            user.remove()
            return user
        return None

    @staticmethod
    def search(search_query, user_state, page, per_page):
        query = User.query

        if (search_query):
            query = query.filter(User.username.like(f"%{search_query}%"))

        if (user_state):
            query = query.filter_by(is_active=user_state == "active")

        return query.paginate(page=page, per_page=per_page, error_out=False)

    @staticmethod
    def all():
        return User.query.all()

    @staticmethod
    def get_by_id(id):
        return User.query.get(id)

    @staticmethod
    def find_by_email(email):
        return User.query.filter_by(email=email).first()
