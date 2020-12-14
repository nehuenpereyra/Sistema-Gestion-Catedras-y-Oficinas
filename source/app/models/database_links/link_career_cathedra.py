
from app.db import db


link_career_cathedra = db.Table("link_career_cathedra",
                          db.Column("career_id", db.Integer, db.ForeignKey("career.id"), primary_key=True),
                          db.Column("cathedra_id", db.Integer, db.ForeignKey("cathedra.id"), primary_key=True))