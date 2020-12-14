
from wtforms.validators import ValidationError


def Unique(class_, query_filter):

    def _unique(form, field):

        object_form = class_.get(form.id.data)
        object_db = class_.query.filter_by(
            **{query_filter: field.data}).first()

        if object_db and object_db != object_form:
            raise ValidationError(f'The value {field.data} is already loaded')

    return _unique
