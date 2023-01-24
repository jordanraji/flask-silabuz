from flask import Blueprint, url_for, flash, redirect, render_template,request
from flask_login import current_user, login_required

from app import db
from app.models.post import Post
from app.forms import PostForm

bp = Blueprint("admin_bp", __name__)

@bp.route('/')
@login_required
def admin():
    return render_template("admin.html")

@bp.route('/post/create', methods=['GET','POST'])
@login_required
def create_post():
    form = PostForm()
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
        return redirect(url_for('views_bp.index'))
    return render_template("create-update-post.html", form=form)

@bp.route('/post/update/<id>', methods=['GET','POST'])
@login_required
def update_post(id):
    form = PostForm()
    post = Post.query.get(id)
    if request.method == 'POST' and form.validate_on_submit():
        if post.user_id == current_user.id:
            post.body = form.body.data
            db.session.commit()
            flash("Se ha actualizado tu post con exito!")
            return redirect(url_for('views_bp.index'))
        else:
            flash("No puedes modificar el post")
    form.body.data = post.body
    return render_template("create-update-post.html", form=form)
    
@bp.route('/post/delete/<id>', methods=['GET'])
@login_required
def delete_post(id):
    post = Post.query.get(id)
    if post.user_id == current_user.id:
        db.session.delete(post)
        db.session.commit()
        flash("Se ha eliminado tu post con exito!")
    return redirect(url_for('views_bp.index'))
    