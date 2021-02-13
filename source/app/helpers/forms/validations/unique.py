
from wtforms.validators import ValidationError


def Unique(class_, query_filter):
    """Returns if the object to create is unique

    Parameters:
    class_ (class): key used to access the message
    query_filter(string): attribute by which it must be unique

    Raises:
    ValidationError: If the attribute value is already in use

   """

    def _unique(form, field):

        object_form = class_.get(form.id.data)
        object_db = class_.query.filter_by(
            **{query_filter: field.data}).first()

        if object_db and object_db != object_form:
            raise ValidationError(
                f'El valor {field.data} se encuentra en uso.')

    return _unique
