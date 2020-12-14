from .translate_form import TranslateForm
from wtforms import SubmitField
from app.models import Role, Permission

from wtforms import IntegerField, StringField, SelectMultipleField

from wtforms.validators import DataRequired, Length, Optional
from app.helpers.forms.validations.unique import Unique

class RoleForm(TranslateForm):

    id = IntegerField()
    name = StringField("Nombre", validators=[ DataRequired(), Unique(Role, "name"), Length(min=3, max=32)], render_kw={'autofocus': True})
    permissions = SelectMultipleField("Permisos", validators=[ Optional()], coerce=int, filters=[lambda value: value or None])
    submit = SubmitField('Enviar')

    def __init__(self, *args, **kwargs):
        super(RoleForm, self).__init__(*args, **kwargs)
        self.permissions.choices = Permission.all() \
            .collect(lambda each: (each.id, each.name))
