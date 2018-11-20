from flask import render_template, redirect, url_for, flash, request, current_app, abort
from flask_login import current_user
from app.models import Tag,Post, Comment, PostView, MessageBoard
from app import db
from . import main
from .forms import CommentForm
from sqlalchemy import func
import time

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

@main.route("/tag/<int:id>", methods=['GET'])
def tag(id):
    page = request.args.get('page', 1, type=int)
    pagination  = Post.query.filter(Post.tags.any(Tag.id == id)).order_by(Post.create_at.desc()).paginate(page,per_page=current_app.config['FLASK_PER_PAGE'],error_out=True)
    posts = pagination.items
    return  render_template('tag.html',current_user=current_user,posts=posts,pagination=pagination,tag_id=id)

@main.route("/post/<int:id>", methods=['GET',"POST"])
def post(id):
    page = request.args.get('page', 1, type=int)
    pagination  = Comment.query.filter_by(post_id=id).order_by(Comment.comment_time.desc()).paginate(page,per_page=current_app.config['FLASK_PER_PAGE'],error_out=True)
    comments = pagination.items
    form = CommentForm()
    if form.validate_on_submit():
        platform = request.user_agent.platform
        browser = request.user_agent.browser
        comment = Comment(post_id=id,user_name=form.user_name.data, email=form.email.data, website=form.website.data, comment=form.comment.data,platform=platform,browser=browser)
        db.session.add(comment)
        db.session.commit()
        flash("评论成功!")
        return redirect(url_for('main.post',id=id))
    post = Post.query.filter_by(id=id).first()
    postview = PostView.query.filter_by(post_id=id,visit_date=time.strftime('%Y-%m-%d',time.localtime(time.time()))).first()
    if postview is None:
        postview = PostView(post_id=id,views=1, visit_date=time.strftime('%Y-%m-%d',time.localtime(time.time())))
    else:
        postview.views += 1
    db.session.add(postview)
    db.session.commit()
    return render_template('post.html', current_user=current_user,post=post, comments=comments, form=form, pagination=pagination,id=id)

@main.route("/timeline")
def timeline():
    page = request.args.get('page', 1, type=int)
    pagination  = Post.query.order_by(Post.create_at.desc()).paginate(page,per_page=current_app.config['FLASK_PER_PAGE'],error_out=True)
    posts = pagination.items
    post_dict = group_posts_by_date(posts)
    return render_template("timeline.html", current_user=current_user, post_dict = post_dict, pagination = pagination)

def group_posts_by_date(posts):
    post_dict = {}
    for post in posts:
        year_month = post.create_at.strftime("%Y-%m")
        if post_dict.get(year_month,None) is None:
            post_dict[year_month] = [post]
        else:
            post_dict[year_month].append(post)
    return post_dict


@main.route("/search", methods=["POST"])
def search():
    if request.method == "POST":
        keyword = request.form.get("keyword")
        like_keyword = "%{}%".format(keyword)
        posts = Post.query.filter(Post.title.like(like_keyword))
        return render_template("search.html", posts=posts, keyword = keyword)
    else:
        abort(404)


@main.route("/about", methods=["GET", "POST"])
def about():
    form = CommentForm()
    if form.validate_on_submit():
        platform = request.user_agent.platform
        browser = request.user_agent.browser
        message_board = MessageBoard(message_type=0,user_name=form.user_name.data, email=form.email.data, website=form.website.data, message=form.comment.data,platform=platform,browser=browser)
        db.session.add(message_board)
        db.session.commit()
        flash("留言成功!")
        return redirect(url_for("main.about"))        
    page = request.args.get('page', 1, type=int)
    pagination  = MessageBoard.query.filter_by(message_type=0).order_by(MessageBoard.message_time.desc()).paginate(page,per_page=current_app.config['FLASK_PER_PAGE'],error_out=True)
    comments = pagination.items
    return render_template("about.html", current_user=current_user, comments = comments, pagination = pagination, form=form)
    