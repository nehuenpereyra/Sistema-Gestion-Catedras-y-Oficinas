from .translate_form import TranslateForm

from app.models import User, Role
from wtforms import SelectField, SubmitField, StringField
from wtforms.validators import Optional, Length


class UserSeeker(TranslateForm):

    user_attributes = SelectField(
        "Campos", validators=[Optional()], coerce=int)
    user_rol = SelectField("Rol", validators=[Optional()], coerce=int)
    search_text = StringField("", validators=[Length(min=3, max=32)])
    submit = SubmitField('Buscar')

    def __init__(self, *args, **kwargs):
        super(UserSeeker, self).__init__(*args, **kwargs)
        self.user_rol.choices = []
        self.user_rol.choices.add((0, "Todos"))
        self.user_rol.choices = self.user_rol.choices + Role.all() \
            .collect(lambda each: (each.id, each.name))
        self.user_attributes.choices = [
            (0, "Nombre"), (1, "Apellido"), (2, "Usuario")]
