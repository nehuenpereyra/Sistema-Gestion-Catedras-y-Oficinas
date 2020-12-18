from .translate_form import TranslateForm

from wtforms import SubmitField
from wtforms import PasswordField
from wtforms.validators import DataRequired, Length


class PasswordChangeForm(TranslateForm):

    user_password = PasswordField("Escriba su nueva contraseña:", validators=[
        DataRequired(), Length(min=8, max=128)])
    submit = SubmitField('Enviar')
