from flask import Flask, render_template, request, flash, url_for, redirect
from flask_wtf import CSRFProtect

from forms import BasicForm, SignupForm, LoginForm
from config import Config
from models import db, User


app = Flask(__name__)
app.config.from_object(Config)

csrf = CSRFProtect()

db.init_app(app)
csrf.init_app(app)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/acerca')
def acerca():
    return render_template("acerca.html")

@app.route('/contacto', methods=['GET','POST'])
def contacto():
    # args = request.args
    # nombre = args.get('nombre', 'Maria')
    # apellido = args.get('apellido', 'Magdalena')
    # nombre_completo = f"{nombre} {apellido}"

    form = BasicForm()
    nombre = "Maria"
    apellido = "Magdalena"
    if request.method == 'POST':
        nombre = form.nombre.data
        apellido = form.apellido.data
    return render_template("contacto.html", form=form, nombre=nombre+" "+apellido)
    
    # http://127.0.0.1:5000/contacto
    # http://127.0.0.1:5000/contacto?nombre=Pedro&apellido=Perez

@app.route('/users', methods=['GET','POST'])
def users():
    # db.create_all()
    users = User.query.all() # SELECT * FROM users;
    return render_template("users.html", users=users)

@app.route('/signup', methods=['GET','POST'])
def signup():
    form = SignupForm()
    if request.method == 'POST' and form.validate_on_submit():
        username = form.username.data.lower()
        email = form.email.data.lower()
        password = form.password.data

        existing_user = User.query.filter_by(email=email).first()
        if not existing_user:
            user = User(
                username=username,
                email=email
            )
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            flash("El usuario se creó correctamente")
            return redirect(url_for('login'))
        else:
            flash("Ya existe un usuario con ese username")
    return render_template("signup.html", form=form)

@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()
        if user and user.check_password(form.password.data):
            flash("¡Bienvenido!")
            return redirect(url_for('admin'))
        else:
            flash("Revisa tus credenciales")
    return render_template("login.html", form=form)

@app.route('/admin')
def admin():
    return render_template("admin.html")