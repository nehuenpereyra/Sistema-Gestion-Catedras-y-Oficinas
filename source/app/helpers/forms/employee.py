from .translate_form import TranslateForm
from wtforms import SubmitField


from wtforms import IntegerField, StringField, SelectField
from wtforms.fields.html5 import EmailField

from wtforms.validators import DataRequired, Length, Optional, Email, ValidationError
from app.helpers.forms.validations.unique import Unique
from app.models import Employee, PendingEmployee

def UniqueEmployee(query_filter):

    def _unique(form, field):

        try:
            (Unique(Employee, query_filter))(form, field)
        except ValidationError as message:
            raise ValidationError(str(message))

        # El dato unico no se encuentra en la tabla empleado o pertence al objeto mismo

        current_employee = Employee.get(form.id.data)

        pending_employee = PendingEmployee.query.filter_by(
            **{query_filter: field.data}).first()

        if pending_employee and not pending_employee.modify_to(current_employee):
            raise ValidationError(f'El valor {field.data} se encuentra pendiente de aprobación.')

        # El dato no se encuentra en la table empleado pendiente o pertenece a un empleado pendiente que modifica al objeto mismo

    return _unique

class EmployeeForm(TranslateForm):

    id = IntegerField()
    name = StringField("Nombre", validators=[ DataRequired(), Length(min=3, max=32)], render_kw={'autofocus': True})
    surname = StringField("Apellido", validators=[ DataRequired(), Length(min=3, max=32)])
    dni = StringField("DNI", validators=[ Optional(), UniqueEmployee("dni"), Length(min=6, max=16)], filters=[lambda value: value or None])
    institutional_email = EmailField("Correo Electrónico Institucional", validators=[ DataRequired(), UniqueEmployee("institutional_email"), Email(), Length(min=3, max=64)])
    secondary_email = EmailField("Correo Electrónico Secundario", validators=[ Optional(), UniqueEmployee("secondary_email"), Email(), Length(min=3, max=64)], filters=[lambda value: value or None])
    type = SelectField("Tipo", validators=[ DataRequired()],
        choices=[(1, 'Docente'), (2, 'No Docente'), (3, 'Empleado Administrativo')]
    )
    submit = SubmitField('Enviar')
