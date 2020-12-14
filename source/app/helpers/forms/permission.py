from .translate_form import TranslateForm
from wtforms import SubmitField
from app.models import Permission, Role

from wtforms import IntegerField, StringField, SelectMultipleField

from wtforms.validators import DataRequired, Length, Optional
from app.helpers.forms.validations.unique import Unique

class PermissionForm(TranslateForm):

    id = IntegerField()
    name = StringField("Nombre", validators=[ DataRequired(), Unique(Permission, "name"), Length(min=3, max=32)], render_kw={'autofocus': True})
    roles = SelectMultipleField("Roles", validators=[ Optional()], coerce=int, filters=[lambda value: value or None])
    submit = SubmitField('Enviar')

    def __init__(self, *args, **kwargs):
        super(PermissionForm, self).__init__(*args, **kwargs)
        self.roles.choices = Role.all() \
            .collect(lambda each: (each.id, each.name))
