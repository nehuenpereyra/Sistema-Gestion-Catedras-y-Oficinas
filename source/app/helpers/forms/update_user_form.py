
from wtforms import PasswordField, BooleanField
from wtforms.validators import Length, ValidationError

from app.helpers.forms.user_form import UserForm


def length_or_empty(min, max):
    """This validator returns true if the field is empty or has between min and max characters, otherwise it throws an exception.

    Keyword arguments:
    min -- minimum number of characters
    max -- maximum number of characters
    """

    def _length_or_empty(form, field):

        message = f'Must be between {min} and {max} characters long.'
        length = len(field.data)

        if (length != 0) and (length < min or length > max):
            raise ValidationError(message)

    return _length_or_empty


class UpdateUserForm(UserForm):

    password = PasswordField('Contraseña',
                             validators=[length_or_empty(min=6, max=20)])

    is_active = BooleanField("Activo", default=True)
