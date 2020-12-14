from .translate_form import TranslateForm
from wtforms import SubmitField
from app.models import Charge, Cathedra, Employee

from wtforms import IntegerField, SelectField
from wtforms.fields.html5 import DateTimeLocalField

from wtforms.validators import DataRequired, Optional

class JobPositionForm(TranslateForm):

    id = IntegerField()
    start_date = DateTimeLocalField("Fecha de Inicio", validators=[ DataRequired()], format='%Y-%m-%dT%H:%M', render_kw={'autofocus': True})
    end_date = DateTimeLocalField("Fecha de Fin", validators=[ Optional()], format='%Y-%m-%dT%H:%M', filters=[lambda value: value or None])
    charge = SelectField("Cargo", validators=[ DataRequired()], coerce=int)
    cathedra = SelectField("Catedra", validators=[ DataRequired()], coerce=int)
    employee = SelectField("Empleado", validators=[ DataRequired()], coerce=int)
    submit = SubmitField('Enviar')

    def __init__(self, *args, **kwargs):
        super(JobPositionForm, self).__init__(*args, **kwargs)
        self.charge.choices = Charge.all() \
            .collect(lambda each: (each.id, each.name))
        self.cathedra.choices = Cathedra.all() \
            .collect(lambda each: (each.id, each.name))
        self.employee.choices = Employee.all() \
            .collect(lambda each: (each.id, each.name))
