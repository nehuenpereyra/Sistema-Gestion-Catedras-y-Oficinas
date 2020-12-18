from app.db import db
from .user_state import UserState


class CareerUser(UserState):

    id = db.Column(db.Integer, db.ForeignKey(
        'user_state.id'), primary_key=True)
    career = db.relationship("Career", back_populates="users", uselist=False)
    career_id = db.Column(db.Integer, db.ForeignKey(
        "career.id"), nullable=True, unique=False)

    __mapper_args__ = {
        'polymorphic_identity': 1
    }

    def is_responsible_of_elements(self):
        return self.career is not None

    def add_responsible_element(self, element):
        self.career = element

    def remove_responsible_element(self, element):
        if self.career is element:
            self.career = None

    def allowed_career_id_list(self):
        if not self.career:
            return []

        return [self.career.id]

    def allowed_cathedra_id_list(self):
        if not self.career:
            return []

        return self.career.cathedras.collect(lambda each: each.id)

    def allowed_employee_id_list(self):
        if not self.career:
            return []

        return self.career.all_employees().collect(lambda each: each.id)

    def allowed_job_position_id_list(self):
        if not self.career:
            return []

        return self.career.all_staff().collect(lambda each: each.id)
