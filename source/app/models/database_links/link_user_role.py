
from app.db import db


link_user_role = db.Table("link_user_role",
                          db.Column("user_id", db.Integer, db.ForeignKey("user.id"), primary_key=True),
                          db.Column("role_id", db.Integer, db.ForeignKey("role.id"), primary_key=True))