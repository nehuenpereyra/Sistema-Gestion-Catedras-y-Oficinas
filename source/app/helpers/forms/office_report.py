from .translate_form import TranslateForm

from app.models import Charge, Workplace, Employee, Office
from wtforms import IntegerField, SelectField, SelectMultipleField, StringField, SubmitField, BooleanField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Length, Optional, Email


class OfficeReport(TranslateForm):

    offices = SelectMultipleField("Oficinas", validators=[
        DataRequired()], coerce=int, filters=[lambda value: value or None])
    charges = SelectMultipleField("Cargos", validators=[
        DataRequired()], coerce=int, filters=[lambda value: value or None])
    institutional_email = EmailField("Correo Electrónico Institucional", validators=[
        Optional(), Email(), Length(max=32)], filters=[lambda value: value if value else None])

    name = StringField("Nombre", validators=[Optional(), Length(max=32)])
    surname = StringField("Apellido", validators=[Optional(), Length(max=32)])
    secondary_email = EmailField("Correo Electrónico Secundario", validators=[
        Optional(), Email(), Length(max=32)], filters=[lambda value: value if value else None])
    dni = StringField("DNI", validators=[Optional(), Length(max=16)])

    show_dni = BooleanField("DNI", default=False)
    show_secondary_email = BooleanField(
        "Correo Electrónico Secundario", default=False)
    submit = SubmitField('Filtrar')

    def __init__(self, *args, **kwargs):
        super(OfficeReport, self).__init__(*args, **kwargs)
        self.offices.choices = Office.all() \
            .collect(lambda each: (each.id, each.name))
        self.charges.choices = Charge.all() \
            .collect(lambda each: (each.id, each.name))
