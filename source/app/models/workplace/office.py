
from app.db import db

from app.models.database_links import link_user_office
from .workplace import Workplace


class Office(Workplace):

    id = db.Column("id", db.Integer, db.ForeignKey(
        'workplace.id'), primary_key=True)
    users = db.relationship(
        "OfficeUser", back_populates="offices", secondary=link_user_office)

    __mapper_args__ = {
        'polymorphic_identity': 2
    }

    def is_office(self):
        return True

    def has_users(self):
        return self.users.any_satisfy(lambda each: not each.is_deleted)

    @staticmethod
    def get_id_string():
        return "office"

    @staticmethod
    def get_label():
        return "Oficina"

    @classmethod
    def search_form(self, name, ids, page, per_page):
        query = self.query
        query = query.filter_by(is_deleted=False)
        query = query.order_by(self.name.asc())
        if not name is None and name != "":
            query = query.filter(self.name.like(f"%{name}%"))

        if ids is not None:
            query = query.filter(self.id.in_(ids))

        return query.paginate(page=page, per_page=per_page, error_out=False)

    @classmethod
    def search(self, show_dni, show_secondary_email, offices, charges_ids, institutional_email, name, surname, secondary_email, dni):

        job_positions = []
        all_job_positions = []
        office_list = []
        charges = {}
        charges_json = {}
        staff = {}
        staff_json = {}
        staff_json_list = []

        offices_obj = []
        for office in offices:
            offices_obj.add(self.get(office))

        for office in offices_obj:
            if not office.all_staff_ordered_by_charge().is_empty():
                for job_position in office.all_staff_ordered_by_charge():
                    if job_position.employee.has_charge(charges_ids, office) and job_position.employee.check_fields(institutional_email, name, surname, secondary_email, dni):
                        job_positions.add(job_position)
                        all_job_positions.add(job_position)

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
                    office_list.add({"office": office, "sttaf": staff})
                    staff_json_list.add({"Oficina": {
                        "Nombre": office.name,
                        "Lugar": office.location,
                        "Email Institucional": office.email,
                        "Telefono": office.phone,
                    }, "Plantel": staff_json})

                staff = {}
                charges = {}
                charges_json = {}
                job_positions = []

        to_export = self.export(all_job_positions,
                                show_dni, show_secondary_email)

        return {"office_list": office_list, "staff_json": staff_json_list, "export": to_export}

    @classmethod
    def export(self, job_positions, show_dni, show_secondary_email):

        data = {}
        contents = {}
        employee = []

        # Los campos en el orden en que se van a mostrar en el pdf y en el excel
        fields = ["Cargo", "Nombre", "Apellido", "Email Institucional"]
        if show_dni:
            fields.add("DNI")
        if show_secondary_email:
            fields.add("Email Secundario")

        index = 0
        for charge_employee in job_positions:
            if not charge_employee.workplace.name in contents:
                contents[charge_employee.workplace.name] = []
            employee = [charge_employee.charge.name, charge_employee.employee.name,
                        charge_employee.employee.surname, charge_employee.employee.institutional_email]
            if show_dni:
                employee.add(charge_employee.employee.dni)
            if show_secondary_email:
                employee.add(charge_employee.employee.secondary_email)
            contents[charge_employee.workplace.name].add(employee)

        return {"fields": fields, "contents": contents}
