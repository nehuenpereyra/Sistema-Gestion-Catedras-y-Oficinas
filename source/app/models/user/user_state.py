from app.db import db

class UserState(db.Model):
    
    id = db.Column("id", db.Integer, primary_key=True)
    type = db.Column(db.Integer, nullable=False)
    user = db.relationship("User", back_populates="user_state", uselist=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    __mapper_args__ = {
        'polymorphic_identity': 0,
        'polymorphic_on':type
    }

    def remove(self):
        if self.id:
            self.is_deleted = True
            self.save()