
from app.db import db


link_user_cathedra = db.Table("link_user_cathedra",
                          db.Column("user_id", db.Integer, db.ForeignKey("cathedra_user.id"), primary_key=True),
                          db.Column("cathedra_id", db.Integer, db.ForeignKey("cathedra.id"), primary_key=True))