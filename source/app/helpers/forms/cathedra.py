from .translate_form import TranslateForm
from wtforms import SubmitField
from app.models import Cathedra, Career

from wtforms import IntegerField, StringField, SelectField
from wtforms.fields.html5 import EmailField

from wtforms.validators import DataRequired, Length, Email, Optional
from app.helpers.forms.validations.unique import Unique

class CathedraForm(TranslateForm):

    id = IntegerField()
    name = StringField("Nombre", validators=[ DataRequired(), Length(min=3, max=64)], render_kw={'autofocus': True})
    email = EmailField("Correo Electrónico Institucional", validators=[ DataRequired(), Unique(Cathedra, "email"), Email(), Length(min=3, max=64)])
    phone = StringField("Teléfono de Contacto", validators=[ DataRequired(), Length(min=3, max=32)])
    location = StringField("Ubicación", validators=[ DataRequired(), Length(min=3, max=64)])
    attention_time = StringField("Hora de Atención", validators=[ DataRequired(), Length(min=3, max=64)])
    career = SelectField("Carrera", validators=[ DataRequired()], coerce=int)
    submit = SubmitField('Enviar')

    def __init__(self, *args, **kwargs):
        super(CathedraForm, self).__init__(*args, **kwargs)
        self.career.choices = Career.all() \
            .collect(lambda each: (each.id, each.name))
