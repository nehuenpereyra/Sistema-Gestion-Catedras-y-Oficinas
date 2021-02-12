
from wtforms.validators import DataRequired, Length

from wtforms import PasswordField
from app.helpers.forms import UserForm

class UserCreateForm(UserForm):
    password = PasswordField("Contraseña", validators=[
                             DataRequired(), Length(min=8, max=128)])