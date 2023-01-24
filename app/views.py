from flask import Blueprint, url_for, flash, redirect, render_template,request

from app import db
from app.models.post import Post
from app.models.user import User
from app.forms import BasicForm
from sqlalchemy import desc

bp = Blueprint("views_bp", __name__)

@bp.route('/')
def index():
    posts = Post.query.order_by(desc(Post.timestamp)).all()
    return render_template("index.html", posts=posts)

@bp.route('/<username>')
def profile(username):
    user = User.query.filter_by(username=username).first()
    # posts = Post.query.filter_by(user_id=user.id).all()
    # posts = Post.query.filter_by(user=user).all()
    posts = user.posts
    return render_template("index.html", posts=posts)

@bp.route('/acerca')
def acerca():
    return render_template("acerca.html")

@bp.route('/contacto', methods=['GET','POST'])
def contacto():
    form = BasicForm()
    nombre = "Maria"
    apellido = "Magdalena"
    if request.method == 'POST':
        nombre = form.nombre.data
        apellido = form.apellido.data
    return render_template("contacto.html", form=form, nombre=nombre+" "+apellido)

@bp.route('/users', methods=['GET','POST'])
def users():
    users = User.query.all() # SELECT * FROM users;
    return render_template("users.html", users=users)