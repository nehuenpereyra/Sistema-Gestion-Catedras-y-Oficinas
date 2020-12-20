from .translate_form import TranslateForm

from app.models import Career
from wtforms import SelectField, SubmitField, StringField
from wtforms.validators import Optional, Length


class CathedraSeeker(TranslateForm):

    name = StringField("Nombre", validators=[Length(min=3, max=32)])
    career_list = SelectField("Carrera", validators=[Optional()], coerce=int)
    submit = SubmitField('Buscar')

    def __init__(self, *args, **kwargs):
        super(CathedraSeeker, self).__init__(*args, **kwargs)
        self.career_list.choices = []
        self.career_list.choices.add((0, "Todas"))
        self.career_list.choices = self.career_list.choices + Career.all() \
            .collect(lambda each: (each.id, each.name))
