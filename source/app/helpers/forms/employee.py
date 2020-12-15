from .translate_form import TranslateForm
from wtforms import SubmitField


from wtforms import IntegerField, StringField, SelectField
from wtforms.fields.html5 import EmailField

from wtforms.validators import DataRequired, Length, Optional, Email

class EmployeeForm(TranslateForm):

    id = IntegerField()
    name = StringField("Nombre", validators=[ DataRequired(), Length(min=3, max=32)], render_kw={'autofocus': True})
    surname = StringField("Apellido", validators=[ DataRequired(), Length(min=3, max=32)])
    dni = StringField("DNI", validators=[ Optional(), Length(min=6, max=16)], filters=[lambda value: value or None])
    institutional_email = EmailField("Correo Electrónico Institucional", validators=[ DataRequired(), Email(), Length(min=3, max=64)])
    secondary_email = EmailField("Correo Electrónico Secundario", validators=[ Optional(), Email(), Length(min=3, max=64)], filters=[lambda value: value or None])
    type = SelectField("Tipo", validators=[ DataRequired()],
        choices=[('docent', 'Docente'), ('not_docent', 'No Docente'), ('administrative', 'Empleado Administrativo')]
    )
    submit = SubmitField('Enviar')
