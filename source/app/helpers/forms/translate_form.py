from flask_wtf import FlaskForm


class TranslateForm(FlaskForm):
    class Meta:
        locales = ['es_ES', 'es']
