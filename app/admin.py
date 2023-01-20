from flask import Blueprint, url_for, flash, redirect, render_template,request
from flask_login import current_user, login_required

from app import db
from app.models.post import Post
from app.forms import CreatePostForm

bp = Blueprint("admin_bp", __name__)

@bp.route('/')
@login_required
def admin():
    print(current_user)
    return render_template("admin.html")

@bp.route('/post/create', methods=['GET','POST'])
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
        return redirect(url_for('views_bp.index'))
    return render_template("create-post.html", form=form)

