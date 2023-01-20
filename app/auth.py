from flask import Blueprint, url_for, flash, redirect, render_template,request
from flask_login import current_user, login_required, login_user, logout_user

from app import login_manager, db
from app.models.user import User
from app.forms import SignupForm, LoginForm

bp = Blueprint("auth_bp", __name__)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id) # User.query.filter_by(id=user_id).first()

@login_manager.unauthorized_handler
def unauthorized():
    flash('Debe iniciar sesión primero')
    return redirect(url_for('auth_bp.login'))

@bp.route('/signup', methods=['GET','POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for("admin_bp.admin"))
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
            return redirect(url_for('auth_bp.login'))
        else:
            flash("Ya existe un usuario con ese username")
    return render_template("signup.html", form=form)

@bp.route('/login', methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("admin_bp.admin"))
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash("¡Bienvenido!")
            return redirect(url_for('admin_bp.admin'))
        else:
            flash("Revisa tus credenciales")
    return render_template("login.html", form=form)

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth_bp.login'))