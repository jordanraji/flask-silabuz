from flask import Flask, render_template, request, flash, url_for, redirect
from flask_wtf import CSRFProtect
from flask_migrate import Migrate
from flask_login import LoginManager, current_user, login_user, logout_user, login_required

from forms import BasicForm, SignupForm, LoginForm, CreatePostForm
from config import Config
from models import db, User, Post


app = Flask(__name__)
app.config.from_object(Config)

csrf = CSRFProtect()
migrate = Migrate()
login_manager = LoginManager()

db.init_app(app)
csrf.init_app(app)
migrate.init_app(app, db)
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id) # User.query.filter_by(id=user_id).first()

@login_manager.unauthorized_handler
def unauthorized():
    flash('Debe iniciar sesión primero')
    return redirect(url_for('login'))

@app.route('/')
def index():
    posts = Post.query.all()
    print(posts)
    return render_template("index.html", posts=posts)

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
    if current_user.is_authenticated:
        return redirect(url_for("admin"))
    form = SignupForm()
    if request.method == 'POST' and form.validate_on_submit():
        username = form.username.data.lower()
        email = form.email.data.lower()
        password = form.password.data
        full_name = form.full_name.data
        description = form.description.data

        existing_user = User.query.filter_by(email=email).first()
        if not existing_user:
            user = User(
                username=username,
                email=email,
                full_name=full_name,
                description=description
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
    if current_user.is_authenticated:
        return redirect(url_for("admin"))
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash("¡Bienvenido!")
            return redirect(url_for('admin'))
        else:
            flash("Revisa tus credenciales")
    return render_template("login.html", form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/admin')
@login_required
def admin():
    print(current_user)
    return render_template("admin.html")

@app.route('/post/create', methods=['GET','POST'])
@login_required
def create_post():
    form = CreatePostForm()
    if request.method == 'POST' and form.validate_on_submit():
        body = form.body.data
        user_id = current_user.id
        post = Post(
            body=body,
            user_id=user_id
        )
        db.session.add(post)
        db.session.commit()
        flash("Se ha publicado tu post con exito!")
        return redirect(url_for('index'))
    return render_template("create-post.html", form=form)


    # http://127.0.0.1:5000/pedro