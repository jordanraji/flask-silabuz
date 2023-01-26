from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, EmailField, PasswordField, TextAreaField
from wtforms.validators import DataRequired, Optional, Regexp
from flask_wtf.file import FileField, FileAllowed

class BasicForm(FlaskForm):
    nombre = StringField('Nombre')
    apellido = StringField('Apellido')
    submit = SubmitField('Enviar')

class LoginForm(FlaskForm):
    email = EmailField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Ingresar")

class UpdateUserForm(FlaskForm):
    username = StringField("Nombre de usuario", validators=[DataRequired()])
    email = EmailField("Correo electrónico", validators=[DataRequired()])
    full_name = StringField("Nombre y apellidos")
    description = StringField("Descripción")
    submit = SubmitField("Enviar")

class UpdatePasswordForm(FlaskForm):
    password = PasswordField("Password", validators=[DataRequired()])

class SignupForm(UpdateUserForm, UpdatePasswordForm):
    pass

class PostForm(FlaskForm):
    body = TextAreaField("Contenido", validators=[DataRequired()])
    submit = SubmitField('Enviar')

class UpdateAvatarForm(FlaskForm):
    file = FileField('Archivo')
    submit = SubmitField('Enviar')
