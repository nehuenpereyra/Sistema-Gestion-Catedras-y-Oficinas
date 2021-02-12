
from wtforms.validators import Optional, Length

from wtforms import PasswordField
from app.helpers.forms import UserForm

class UserUpdateForm(UserForm):
    password = PasswordField("Contraseña", validators=[
                             Optional(), Length(min=8, max=128)],
                             filters=[lambda value: value or None])