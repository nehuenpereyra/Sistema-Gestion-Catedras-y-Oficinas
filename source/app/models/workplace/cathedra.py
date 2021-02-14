
from app.db import db
from app.models.database_links import link_user_cathedra
from .workplace import Workplace


class Cathedra(Workplace):

    id = db.Column("id", db.Integer, db.ForeignKey(
        'workplace.id'), primary_key=True)
    attention_time = db.Column("attention_time", db.String(
        64), nullable=False, unique=False)
    users = db.relationship(
        "CathedraUser", back_populates="cathedras", secondary=link_user_cathedra)
    career = db.relationship(
        "Career", back_populates="cathedras", uselist=False)
    career_id = db.Column("career_id", db.Integer, db.ForeignKey(
        "career.id"), nullable=False, unique=False)

    __mapper_args__ = {
        'polymorphic_identity': 1
    }

    def is_cathedra(self):
        return True

    def has_users(self):
        return self.users.any_satisfy(lambda each: not each.is_deleted)

    @staticmethod
    def get_id_string():
        return "cathedra"

    @staticmethod
    def get_label():
        return "Cátedra"

    @classmethod
    def search_form(self, career_list_id, name, ids, page, per_page):
        query = self.query
        query = query.filter_by(is_deleted=False)
        query = query.order_by(self.name.asc())
        if not name is None and name != "":
            query = query.filter(self.name.like(f"%{name}%"))

        if not career_list_id is None and career_list_id != 0:
            query = query.filter(self.career.has(
                id=career_list_id))

        if ids is not None:
            query = query.filter(self.id.in_(ids))

        return query.paginate(page=page, per_page=per_page, error_out=False)

    def update(self, name, email, phone, location, attention_time, career):
        self.name = name
        self.email = email
        self.phone = phone
        self.location = location
        self.attention_time = attention_time
        self.career = career
        self.save()

    @classmethod
    def search(self, show_dni, show_secondary_email, cathedras, employee_type, charges_ids, institutional_email, name, surname, secondary_email, dni):

        job_positions = []
        cathedra_list = []
        charges = {}
        charges_json = {}
        staff = {}
        staff_json = {}
        staff_json_list = []

        cathedras_obj = []
        for cathedra in cathedras:
            cathedras_obj.add(self.get(cathedra))

        for cathedra in cathedras_obj:
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
                    charges[charge_employee.charge.name].add(charge_employee)
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
                    cathedra_list.add({"cathedra": cathedra, "sttaf": staff})
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

        return {"cathedra_list": cathedra_list, "staff_json": staff_json_list}
