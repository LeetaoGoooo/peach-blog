from flask import render_template, redirect, url_for, flash, request, current_app
from flask_login import current_user
from app.models import Tag,Post
from . import main

@main.app_context_processor
def peach_blog_menu():
    tags = Tag.query.all()
    return dict(peach_blog_menu=tags)


@main.route("/", methods=['GET'])
def index():
    page = request.args.get('page', 1, type=int)
    pagination  = Post.query.order_by(Post.create_at.desc()).paginate(page,per_page=current_app.config['FLASK_PER_PAGE'],error_out=True)
    posts = pagination.items
    return  render_template('index.html',current_user=current_user,posts=posts,pagination=pagination)
