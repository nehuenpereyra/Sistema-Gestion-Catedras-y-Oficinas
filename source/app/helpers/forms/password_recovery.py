from .translate_form import TranslateForm

from wtforms import SubmitField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Length, Optional


class PasswordRecoveryForm(TranslateForm):

    user_email = EmailField("Ingrese el email institucional de la cuenta a recuperar:", validators=[
        DataRequired(), Length(min=3, max=64)])
    submit = SubmitField('Enviar')
