from .translate_form import TranslateForm
from wtforms import SubmitField
from app.models import Office

from wtforms import IntegerField, StringField
from wtforms.fields.html5 import EmailField

from wtforms.validators import DataRequired, Length, Email
from app.helpers.forms.validations.unique import Unique

class OfficeForm(TranslateForm):

    id = IntegerField()
    name = StringField("Nombre", validators=[ DataRequired(), Length(min=3, max=64)], render_kw={'autofocus': True})
    email = EmailField("Correo Electrónico Institucional", validators=[ DataRequired(), Unique(Office, "email"), Email(), Length(min=3, max=64)])
    phone = StringField("Teléfono de Contacto", validators=[ DataRequired(), Length(min=3, max=32)])
    location = StringField("Ubicación", validators=[ DataRequired(), Length(min=3, max=64)])
    submit = SubmitField('Enviar')

