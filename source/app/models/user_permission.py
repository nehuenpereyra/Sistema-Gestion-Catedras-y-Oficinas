from sqlalchemy.ext.hybrid import hybrid_property

from app.db import db

link_role_permission = db.Table("link_role_permission",
                                db.Column("role_id", db.Integer, db.ForeignKey(
                                    "user_role.id"), primary_key=True),
                                db.Column("permission_id", db.Integer, db.ForeignKey(
                                    "user_permission.id"), primary_key=True),
                                )


class UserPermission(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True, nullable=False)
    roles = db.relationship(
        "UserRole", secondary=link_role_permission, back_populates="permissions")

    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()
