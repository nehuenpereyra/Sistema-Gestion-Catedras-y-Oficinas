from .translate_form import TranslateForm
from wtforms import SubmitField
from app.models import User, Role

from wtforms import IntegerField, StringField, SelectMultipleField, PasswordField
from wtforms.fields.html5 import EmailField

from wtforms.validators import DataRequired, Length, Email, Optional, ValidationError
from app.helpers.forms.validations.unique import Unique


def role_without_elements():
    """Returns if the user contains dependencies according to the assigned roles

    Raises:
    ValidationError: If the user contains dependencies according to the assigned roles

    """

    def _role_without_elements(form, field):

        if form.id.data:
            user = User.get(form.id.data)
            roles = Role.get_all(form.roles.data)
            if user.responsible_role_changed(roles) and user.is_responsible_of_elements():
                raise ValidationError(
                    'El rol no puede ser modificado mientras contenga dependencias.'
                )

    return _role_without_elements

def role_selection():
    """Throws an exception if more than 2 roles are selected or 2 are selected and one of them is not the Visitor role

    Raises:
    ValidationError: More than 2 roles are selected or 2 are selected and one of them is not the Visitor role

    """

    def _role_selection(form, field):
        roles = Role.get_all(field.data)

        if roles.size() > 1:
            if roles.size() > 2:
                raise ValidationError("A lo sumo se puede tener 2 roles, siendo uno de ellos el rol Visitante")
            elif not roles.any_satisfy(lambda each: each.name == "Visitante"):
                raise ValidationError("Solo el rol Visitante puede estar en conjunto con otro rol")

    return _role_selection

class UserForm(TranslateForm):

    id = IntegerField()
    name = StringField("Nombre", validators=[DataRequired(), Length(
        min=3, max=32)], render_kw={'autofocus': True})
    surname = StringField("Apellido", validators=[
                          DataRequired(), Length(min=3, max=32)])
    username = StringField("Usuario", validators=[
                           DataRequired(), Length(min=3, max=32), Unique(User, "username")])
    institutional_email = EmailField("Correo Electrónico Institucional", validators=[
                                     DataRequired(), Email(), Length(min=3, max=64), Unique(User, "institutional_email")])
    secondary_email = EmailField("Correo Electrónico Secundario", validators=[
                                 DataRequired(), Email(), Length(min=3, max=64)])
    roles = SelectMultipleField(
        "Roles", validators=[DataRequired(), role_without_elements(), role_selection()], coerce=int)
    submit = SubmitField('Enviar')

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.roles.choices = Role.all() \
            .collect(lambda each: (each.id, each.name))
