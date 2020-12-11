from .translate_form import TranslateForm
from wtforms import StringField, SubmitField, RadioField
from wtforms.validators import DataRequired


class UserSeekerForm(TranslateForm):
    search_query = StringField('Buscar')
    user_state = RadioField(
        '', choices=[('active', 'Activos'), ('blocked', 'Bloqueados')])
    submit = SubmitField('Buscar')
