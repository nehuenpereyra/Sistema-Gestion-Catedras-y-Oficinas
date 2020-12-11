from sqlalchemy.ext.hybrid import hybrid_property

from app.db import db
from app.models.user_permission import UserPermission, link_role_permission

link_user_role = db.Table("link_user_role",
                          db.Column("user_id", db.Integer, db.ForeignKey(
                              "user.id"), primary_key=True),
                          db.Column("role_id", db.Integer, db.ForeignKey("user_role.id"), primary_key=True))


class UserRole(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True, nullable=False)
    users = db.relationship(
        "User", secondary=link_user_role, back_populates="roles")
    permissions = db.relationship(
        "UserPermission", secondary=link_role_permission, back_populates="roles")

    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()
