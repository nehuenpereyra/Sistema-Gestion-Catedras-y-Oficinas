import phonenumbers
from wtforms.validators import ValidationError

def Telephone():
    def _valid_number(form, field):
        message = f'No es un numero valido.'
        try:
            if not (phonenumbers.is_valid_number(phonenumbers.parse(field.data, "AR"))):
                raise ValidationError(message)
        except:
            raise ValidationError(message)

    return _valid_number