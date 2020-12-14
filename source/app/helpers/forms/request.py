from .translate_form import TranslateForm
from wtforms import SubmitField
from app.models import User, RequestType

from wtforms import IntegerField, StringField, BooleanField, SelectField
from wtforms.fields.html5 import DateTimeLocalField

from wtforms.validators import DataRequired, Length, Optional

class RequestForm(TranslateForm):

    id = IntegerField()
    content = StringField("Contenido", validators=[ DataRequired(), Length(min=3, max=200)], render_kw={'autofocus': True})
    is_resolved = BooleanField("Resuelto", validators=[ Optional()], filters=[lambda value: value or None], default=False)
    receive_email = BooleanField("Recibir Correo Electrónico", validators=[ Optional()], filters=[lambda value: value or None], default=False)
    timestamp = DateTimeLocalField("Fecha de Creación", validators=[ DataRequired()], format='%Y-%m-%dT%H:%M')
    user = SelectField("Usuario", validators=[ DataRequired()], coerce=int)
    request_type = SelectField("Tipo de Solicitud", validators=[ DataRequired()], coerce=int)
    submit = SubmitField('Enviar')

    def __init__(self, *args, **kwargs):
        super(RequestForm, self).__init__(*args, **kwargs)
        self.user.choices = User.all() \
            .collect(lambda each: (each.id, each.name))
        self.request_type.choices = RequestType.all() \
            .collect(lambda each: (each.id, each.name))
