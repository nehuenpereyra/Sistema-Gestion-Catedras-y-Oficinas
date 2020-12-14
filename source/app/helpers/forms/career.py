from .translate_form import TranslateForm
from wtforms import SubmitField
from app.models import Career

from wtforms import IntegerField, StringField

from wtforms.validators import DataRequired, Length, Optional
from app.helpers.forms.validations.unique import Unique

class CareerForm(TranslateForm):

    id = IntegerField()
    name = StringField("Nombre", validators=[ DataRequired(), Unique(Career, "name"), Length(min=3, max=64)], render_kw={'autofocus': True})
    submit = SubmitField('Enviar')

