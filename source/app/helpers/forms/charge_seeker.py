from .translate_form import TranslateForm

from wtforms import SelectField, SubmitField, StringField
from wtforms.validators import Optional, Length


class ChargeSeeker(TranslateForm):

    name = StringField("Nombre", validators=[Length(min=3, max=32)])
    charge_type = SelectField("Cargo", validators=[Optional()], coerce=int)
    submit = SubmitField('Buscar')

    def __init__(self, *args, **kwargs):
        super(ChargeSeeker, self).__init__(*args, **kwargs)
        self.charge_type.choices = [
            (0, "Todos"), (1, "Docentes"), (2, "No Docentes")]
