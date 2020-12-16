from .translate_form import TranslateForm
from wtforms import SubmitField
from app.models import Role

from wtforms import IntegerField, StringField, SelectMultipleField, PasswordField
from wtforms.fields.html5 import EmailField

from wtforms.validators import DataRequired, Length, Email, Optional

class UserForm(TranslateForm):

    id = IntegerField()
    name = StringField("Nombre", validators=[ DataRequired(), Length(min=3, max=32)], render_kw={'autofocus': True})
    surname = StringField("Apellido", validators=[ DataRequired(), Length(min=3, max=32)])
    username = StringField("Usuario", validators=[ DataRequired(), Length(min=3, max=32)])
    password = PasswordField("Contraseña", validators=[ DataRequired(), Length(min=8, max=128)])
    institutional_email = EmailField("Correo Electrónico Institucional", validators=[ DataRequired(), Email(), Length(min=3, max=64)])
    secondary_email = EmailField("Correo Electrónico Secundario", validators=[ DataRequired(), Email(), Length(min=3, max=64)])
    roles = SelectMultipleField("Roles", validators=[ DataRequired()], coerce=int)
    submit = SubmitField('Enviar')

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.roles.choices = Role.all() \
            .collect(lambda each: (each.id, each.name))
