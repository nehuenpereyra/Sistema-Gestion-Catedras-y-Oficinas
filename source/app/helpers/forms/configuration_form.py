from .translate_form import TranslateForm
from wtforms import StringField, SubmitField, BooleanField, IntegerField
from wtforms.validators import DataRequired, Email, Length, NumberRange
from wtforms.widgets import TextArea
from wtforms.fields.html5 import EmailField


class ConfigurationForm(TranslateForm):
    title = StringField('Titulo', validators=[DataRequired(), Length(max=30)])
    description = StringField('Descripción', validators=[
                              DataRequired(), Length(max=160)], widget=TextArea())
    contact_email = EmailField('Email de contacto', validators=[
        DataRequired(), Email(), Length(max=30)])
    items_per_page = IntegerField(
        'Numero de elementos en la paginación', validators=[DataRequired(), NumberRange(min=1)])
    enabled_site = BooleanField(
        'Sitio habilitado', default=False)
    submit = SubmitField('Actualizar')
