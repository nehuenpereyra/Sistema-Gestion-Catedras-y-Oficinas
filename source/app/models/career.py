
from app.db import db


class Career(db.Model):

    id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column("name", db.String(64), nullable=False, unique=True)
    users = db.relationship("CareerUser", back_populates="career")
    cathedras = db.relationship("Cathedra", back_populates="career")
    is_deleted = db.Column(db.Boolean, nullable=False, default=False)

    def get_cathedras(self):
        return self.cathedras.select(lambda each: not each.is_deleted)

    def set_cathedras(self, cathedras):
        self.cathedras = self.cathedras.select(
            lambda each: each.is_deleted) + cathedras

    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()

    def update(self, name):
        self.name = name
        self.save()

    def remove(self):
        if self.id:
            self.is_deleted = True
            self.save()

    @classmethod
    def delete(self, id):
        career = self.query.get(id)
        if career:
            career.remove()
            return career
        return None

    @classmethod
    def all(self):
        query = self.query
        query = query.filter_by(is_deleted=False)
        query = query.order_by(self.name.asc())
        return query.all()

    @classmethod
    def all_paginated(self, page, per_page, ids=None, only_ids=True):

        query = self.query
        query = query.filter_by(is_deleted=False)
        query = query.order_by(self.name.asc())

        if ids is not None:
            if only_ids:
                query = query.filter(self.id.in_(ids))
            else:
                query = query.filter(~self.id.in_(ids))

        return query.paginate(page=page, per_page=per_page, error_out=False)

    @classmethod
    def get(self, id):
        career = self.query.get(id)
        return career if career and career.is_deleted == False else None

    @classmethod
    def get_all(self, ids):
        if not ids:
            return []
        query = self.query
        query = query.filter_by(is_deleted=False)
        return query.filter(self.id.in_(ids)).all()

    @classmethod
    def find_by_name(self, name):
        query = self.query.order_by(self.name.asc())
        return query.filter_by(name=name, is_deleted=False).all()

    @classmethod
    def search(self, show_dni, show_secondary_email, careers, employee_type, charges_ids, institutional_email, name, surname, secondary_email, dni):

        job_positions = []
        cathedra_list = []
        career_list = []
        charges = {}
        charges_json = {}
        staff = {}
        staff_json = {}
        staff_json_list = []
        staff_json_career = []

        careers_obj = []
        for career in careers:
            careers_obj.add(self.get(career))

        for career in careers_obj:
            for cathedra in career.get_cathedras():
                if not cathedra.all_staff_ordered_by_charge().is_empty():
                    for job_position in cathedra.all_staff_ordered_by_charge():
                        if job_position.employee.has_charge(charges_ids, cathedra) and job_position.employee.check_fields(institutional_email, name, surname, secondary_email, dni):
                            # Todos
                            if employee_type == 0:
                                job_positions.add(job_position)
                            # Tipo Docente
                            if employee_type == 1 and job_position.employee.is_docent():
                                job_positions.add(job_position)
                            # Tipo No Docente
                            if employee_type == 2 and job_position.employee.is_not_docent():
                                job_positions.add(job_position)

                    for charge_employee in job_positions:
                        if not charge_employee.charge.name in charges:
                            charges[charge_employee.charge.name] = []
                        charges[charge_employee.charge.name].add(
                            charge_employee)
                        charges_json[charge_employee.charge.name] = {
                            "Nombre": charge_employee.employee.name,
                            "Apellido": charge_employee.employee.surname,
                            "Cargo": charge_employee.charge.name,
                            "Email Institucional": charge_employee.employee.institutional_email}
                        if show_dni:
                            charges_json[charge_employee.charge.name].update({
                                "DNI": charge_employee.employee.dni if not charge_employee.employee.dni is None else ""
                            })
                        if show_secondary_email:
                            charges_json[charge_employee.charge.name].update({
                                "Email Secundario": charge_employee.employee.secondary_email if not charge_employee.employee.secondary_email is None else ""
                            })

                    for key, values in charges.items():
                        if not values.first().employee.get_label() in staff:
                            staff[values.first().employee.get_label()] = {
                                key: charges[key]}
                            staff_json[values.first().employee.get_label()] = {
                                key: charges_json[key]
                            }
                        else:
                            staff[values.first().employee.get_label()].update(
                                {key: charges[key]})
                            staff_json[values.first().employee.get_label()].update(
                                {key: charges_json[key]})

                    if not list(staff.keys()).is_empty():
                        cathedra_list.add(
                            {"cathedra": cathedra, "sttaf": staff})
                        staff_json_list.add({"Cátedra": {
                            "Nombre": cathedra.name,
                            "Horario de apertura": cathedra.attention_time,
                            "Lugar": cathedra.location,
                            "Email Institucional": cathedra.email,
                            "Telefono": cathedra.phone,
                        }, "Plantel": staff_json})

                    staff = {}
                    charges = {}
                    charges_json = {}
                    job_positions = []

            if not cathedra_list.is_empty():
                career_list.add({"Carrera": career, "Catedras": cathedra_list})
                staff_json_career.add(
                    {"Carrera": career.name, "Cátedras": staff_json_list})
            cathedra_list = []
        return {"career_list": career_list, "staff_json": staff_json_career}
