from .translate_form import TranslateForm
from wtforms import SubmitField
from app.models import RequestType

from wtforms import IntegerField, StringField, BooleanField

from wtforms.validators import DataRequired, Length, Optional
from app.helpers.forms.validations.unique import Unique

class RequestTypeForm(TranslateForm):

    id = IntegerField()
    name = StringField("Nombre", validators=[ DataRequired(), Unique(RequestType, "name"), Length(min=3, max=32)], render_kw={'autofocus': True})
    message = StringField("Mensaje Informativo", validators=[ DataRequired(), Length(min=3, max=200)])
    state = BooleanField("Estado", validators=[ Optional()], filters=[lambda value: value or None], default=True)
    submit = SubmitField('Enviar')

