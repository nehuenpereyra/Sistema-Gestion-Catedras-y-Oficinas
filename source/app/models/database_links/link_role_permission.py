
from app.db import db


link_role_permission = db.Table("link_role_permission",
                          db.Column("role_id", db.Integer, db.ForeignKey("role.id"), primary_key=True),
                          db.Column("permission_id", db.Integer, db.ForeignKey("permission.id"), primary_key=True))