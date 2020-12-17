from .translate_form import TranslateForm
from wtforms import StringField, SubmitField, BooleanField, IntegerField, PasswordField
from wtforms.validators import DataRequired, Email, Length, NumberRange
from wtforms.widgets import TextArea
from wtforms.fields.html5 import EmailField


class ConfigurationForm(TranslateForm):
    mail_contact = EmailField('Email de contacto', validators=[
        DataRequired(), Email(), Length(max=30)])
    mail_server = StringField('Mail del servidor de correo', validators=[
        DataRequired(), Length(max=160)])
    mail_port = IntegerField(
        'Puerto del servidor de correo', validators=[DataRequired(), NumberRange(min=1)])
    mail_password = PasswordField("Contraseña del email de contacto", validators=[ DataRequired(), Length(min=8, max=128)])
    items_per_page = IntegerField(
        'Numero de elementos en la paginación', validators=[DataRequired(), NumberRange(min=1)])
    submit = SubmitField('Actualizar')
