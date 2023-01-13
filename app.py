from flask import Flask, render_template, request
from flask_wtf import CSRFProtect

from forms import BasicForm
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

@app.route('/users')
def users():
    # db.create_all()
    users = User.query.all() # SELECT * FROM users;
    return render_template("users.html", users=users)
