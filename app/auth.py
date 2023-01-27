from flask import Blueprint, url_for, flash, redirect, render_template, request, current_app
from flask_login import current_user, login_required, login_user, logout_user

from app import login_manager, db, http_auth, jwt
from app.models.user import User
from app.forms import SignupForm, LoginForm, UpdatePasswordForm, UpdateUserForm, UpdateAvatarForm
from werkzeug.utils import secure_filename

import os

bp = Blueprint("auth_bp", __name__)

@jwt.user_identity_loader
def user_identity_lookup(user):
    return user.id

@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return User.query.filter_by(id=identity).one_or_none()

@http_auth.verify_password
def verify_password(email, password):
    user = User.query.filter_by(email=email).first()
    if user and user.check_password(password):
        return user
    return False

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

@bp.route('/profile/update-avatar', methods=['GET','POST'])
@login_required
def update_avatar():
    form = UpdateAvatarForm()
    if request.method == 'POST' and form.validate_on_submit():
        file = form.file.data
        filename = secure_filename(file.filename)
        if filename != '':
            _, ext = os.path.splitext(filename)
            path = os.path.join(current_app.root_path, 'static', 'img', 'avatars', str(current_user.id)+ext)
            file.save(path)
            current_user.avatar_url = f"{request.url_root}static/img/avatars/{str(current_user.id)+ext}"
            db.session.commit()
            flash("Se actualizó tu avatar con exito")
            return redirect(url_for('admin_bp.admin'))
        
    return render_template("update-avatar.html", form=form)
