
from app.db import db

from app.models.database_links import link_user_office
from .user_state import UserState

class OfficeUser(UserState):
    
    id = db.Column("id", db.Integer, db.ForeignKey('user_state.id'), primary_key=True)
    offices = db.relationship("Office", back_populates="users", secondary=link_user_office)

    __mapper_args__ = {
        'polymorphic_identity': 3
    }

    def allowed_office_id_list(self):
        return self.offices.collect(lambda each: each.id)
    
    def allowed_employee_id_list(self):
        return self.offices.flat_collect(lambda each: each.all_employees()) \
            .remove_duplicated() \
            .collect(lambda each: each.id)

    def allowed_job_position_id_list(self):
        return self.offices.flat_collect(lambda each: each.all_staff()) \
            .collect(lambda each: each.id)