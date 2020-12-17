from .translate_form import TranslateForm
from wtforms import SubmitField
from app.models import Charge

from wtforms import IntegerField, StringField, BooleanField

from wtforms.validators import DataRequired, Length, Optional
from app.helpers.forms.validations.unique import Unique

class ChargeForm(TranslateForm):

    id = IntegerField()
    name = StringField("Nombre", validators=[ DataRequired(), Unique(Charge, "name"), Length(min=3, max=64)], render_kw={'autofocus': True})
    is_docent = BooleanField("Es cargo docente", validators=[ Optional()], filters=[lambda value: value or False], default=False)
    order = IntegerField("Orden", validators=[ DataRequired()])
    submit = SubmitField('Enviar')

