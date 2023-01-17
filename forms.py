from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, EmailField, PasswordField
from wtforms.validators import DataRequired, Optional, Regexp

class BasicForm(FlaskForm):
    nombre = StringField('Nombre')
    apellido = StringField('Apellido')
    submit = SubmitField('Enviar')

class LoginForm(FlaskForm):
    email = EmailField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Ingresar")

class SignupForm(FlaskForm):
    username = StringField("Nombre de usuario", validators=[DataRequired()])
    email = EmailField("Correo electrónico", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Crear cuenta")
