
from app.db import db

from app.models.database_links import link_user_cathedra
from .user_state import UserState


class CathedraUser(UserState):

    id = db.Column("id", db.Integer, db.ForeignKey(
        'user_state.id'), primary_key=True)
    cathedras = db.relationship(
        "Cathedra", back_populates="users", secondary=link_user_cathedra)

    __mapper_args__ = {
        'polymorphic_identity': 2
    }

    def is_responsible_of_elements(self):
        return not self.cathedras.is_empty()

    def add_responsible_element(self, element):
        self.cathedras.add(element)

    def remove_responsible_element(self, element):
        self.cathedras.remove(element)

    def allowed_cathedra_id_list(self):
        return self.cathedras.collect(lambda each: each.id)

    def allowed_employee_id_list(self):
        return self.cathedras.flat_collect(lambda each: each.all_employees()) \
            .remove_duplicated() \
            .collect(lambda each: each.id)

    def allowed_job_position_id_list(self):
        return self.cathedras.flat_collect(lambda each: each.all_staff()) \
            .collect(lambda each: each.id)
