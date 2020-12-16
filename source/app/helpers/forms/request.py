from .translate_form import TranslateForm
from wtforms import SubmitField
from app.models import User, RequestType

from wtforms import IntegerField, StringField, BooleanField, SelectField
from wtforms.fields.html5 import DateTimeLocalField

from wtforms.validators import DataRequired, Length, Optional
from flask_ckeditor import CKEditorField

class RequestForm(TranslateForm):

    id = IntegerField()
    content = CKEditorField("Contenido", validators=[ DataRequired(), Length(min=3, max=200)], render_kw={'autofocus': True})
    receive_email = BooleanField("Recibir Correo Electrónico", validators=[ Optional()], filters=[lambda value: value or None], default=False)
    submit = SubmitField('Enviar')

