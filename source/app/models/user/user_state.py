
from app.db import db


class UserState(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.Integer, nullable=False)
    user = db.relationship("User", back_populates="state", uselist=False)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'user.id'), nullable=False, unique=False)

    __mapper_args__ = {
        'polymorphic_identity': 0,
        'polymorphic_on': type
    }

    def add_responsible_element(self, element):
        pass

    def allowed_career_id_list(self):
        return []

    def allowed_cathedra_id_list(self):
        return []

    def allowed_office_id_list(self):
        return []

    def allowed_employee_id_list(self):
        return []

    def allowed_job_position_id_list(self):
        return []

    def remove(self):
        if self.id:
            self.is_deleted = True
            self.save()

    # @property
    # def name(self):
    #     return self.user.name
