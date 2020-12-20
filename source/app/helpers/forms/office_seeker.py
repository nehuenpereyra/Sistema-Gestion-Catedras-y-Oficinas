from .translate_form import TranslateForm

from app.models import Career
from wtforms import SubmitField, StringField
from wtforms.validators import Optional, Length


class OfficeSeeker(TranslateForm):

    name = StringField("Nombre", validators=[Length(min=3, max=32)])
    submit = SubmitField('Buscar')
