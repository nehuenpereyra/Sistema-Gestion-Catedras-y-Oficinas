from .translate_form import TranslateForm

from app.models import User, Charge
from wtforms import SelectField, SubmitField, StringField
from wtforms.validators import Optional, Length


class EmployeeSeeker(TranslateForm):

    employee_attributes = SelectField(
        "Campos", validators=[Optional()], coerce=int)
    search_text = StringField("", validators=[Length(min=3, max=32)])
    employee_charge = SelectField("Cargo", validators=[Optional()], coerce=int)
    employee_type = SelectField(
        "Empleado", validators=[Optional()], coerce=int)
    submit = SubmitField('Buscar')

    def __init__(self, *args, **kwargs):
        super(EmployeeSeeker, self).__init__(*args, **kwargs)
        self.employee_charge.choices = []
        self.employee_charge.choices.add((0, "Todos"))
        self.employee_charge.choices = self.employee_charge.choices + Charge.all() \
            .collect(lambda each: (each.id, each.name))
        self.employee_attributes.choices = [
            (0, "Nombre y Apellido"), (1, "Nombre"), (2, "Apellido")]
        self.employee_type.choices = [
            (0, "Todos"), (1, "Docentes"), (2, "No Docentes"), (3, "Administrativos")]
