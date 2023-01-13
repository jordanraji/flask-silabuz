from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField

class BasicForm(FlaskForm):
    nombre = StringField('Nombre')
    apellido = StringField('Apellido')
    submit = SubmitField('Enviar')