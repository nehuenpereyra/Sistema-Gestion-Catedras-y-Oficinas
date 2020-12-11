from wtforms import PasswordField
from wtforms.validators import DataRequired, Length

from app.helpers.forms.user_form import UserForm


class SignupForm(UserForm):

    password = PasswordField('Contraseña',
                             validators=[DataRequired(), Length(min=6, max=20)])
