from flask import Blueprint, url_for, flash, redirect, render_template,request
from flask_login import current_user, login_required, login_user, logout_user

from app import login_manager, db
from app.models.user import User
from app.forms import SignupForm, LoginForm, UpdatePasswordForm, UpdateUserForm

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
            user.set_avatar()
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

@bp.route('/profile/update', methods=['GET','POST'])
@login_required
def update_profile():
    form = UpdateUserForm()
    user = current_user
    if request.method == 'POST' and form.validate_on_submit():
        user.full_name = form.full_name.data
        user.email = form.email.data
        user.description = form.description.data
        user.username = form.username.data
        db.session.commit()
        flash("Se cambió tu información con éxito")
        return redirect(url_for('views_bp.profile', username=user.username))
    form.full_name.data = user.full_name
    form.email.data = user.email
    form.description.data = user.description
    form.username.data = user.username
    return render_template("update-user.html", form=form)

@bp.route('/password/update', methods=['GET','POST'])
@login_required
def update_password():
    form = UpdatePasswordForm()
    if request.method == 'POST' and form.validate_on_submit():
        user = current_user
        password = form.password.data
        user.set_password(password)
        db.session.commit()
        flash("Se cambió tu contraseña con éxito")
        return redirect(url_for('views_bp.profile', username=user.username))
    return render_template("update-password.html", form=form)

@bp.route('/profile/delete')
@login_required
def delete_profile():
    user = current_user
    for post in user.posts:
        db.session.delete(post)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('auth_bp.logout'))


# https://secure.gravatar.com/avatar/4242513ffd7fcaa66569f4a37f488fee?s=100&d=identicon&r=g