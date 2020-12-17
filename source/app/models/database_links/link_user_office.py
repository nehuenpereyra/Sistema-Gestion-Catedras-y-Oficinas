
from app.db import db


link_user_office = db.Table("link_user_office",
                          db.Column("user_id", db.Integer, db.ForeignKey("office_user.id"), primary_key=True),
                          db.Column("office_id", db.Integer, db.ForeignKey("office.id"), primary_key=True))