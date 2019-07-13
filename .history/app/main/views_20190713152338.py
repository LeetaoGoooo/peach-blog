from flask import render_template, redirect, url_for, flash, request, current_app, abort
from flask_login import current_user
from app.models import Tag, Post, Comment, PostView, MessageBoard, FriendLink, History
from app import db
from . import main
from .forms import CommentForm
from sqlalchemy import func
import time
from datetime import datetime
from collections import OrderedDict
from werkzeug.contrib.atom import AtomFeed
import misaka as markdown
from urllib.parse import urljoin


@main.app_context_processor
def peach_blog_menu():
    tags = Tag.query.all()
    return dict(peach_blog_menu=tags)


@main.route("/", methods=['GET'])
def index():
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.order_by(Post.create_at.desc()).paginate(
        page, per_page=current_app.config['FLASK_PER_PAGE'], error_out=True)
    posts = pagination.items
    return render_template('index.html', current_user=current_user, posts=posts, pagination=pagination)


@main.route("/tag/<string:tag>", methods=['GET'])
def tag(tag):
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.filter(Post.tags.any(Tag.tag == tag)).order_by(Post.create_at.desc(
    )).paginate(page, per_page=current_app.config['FLASK_PER_PAGE'], error_out=True)
    posts = pagination.items
    return render_template('tag.html', current_user=current_user, posts=posts, pagination=pagination, tag=tag)


@main.route("/post/<string:title>", methods=['GET', "POST"])
def post(title):
    page = request.args.get('page', 1, type=int)
    post = Post.query.filter_by(title=title).first()
    id = post.id
    pagination = Comment.query.filter_by(post_id=id).order_by(Comment.comment_time.desc(
    )).paginate(page, per_page=current_app.config['FLASK_PER_PAGE'], error_out=True)
    comments = pagination.items
    form = CommentForm()
    if form.validate_on_submit():
        platform = request.user_agent.platform
        browser = request.user_agent.browser
        comment = Comment(post_id=id, user_name=form.user_name.data, email=form.email.data, website=form.website.data,
                          comment=form.comment.data, platform=platform, browser=browser, comment_time=datetime.now())
        db.session.add(comment)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
        flash("评论成功!")
        return redirect(url_for('main.post', title=title))
    post = Post.query.filter_by(id=id).first()
    postview = PostView.query.filter_by(post_id=id, visit_date=time.strftime(
        '%Y-%m-%d', time.localtime(time.time()))).first()
    if postview is None:
        postview = PostView(post_id=id, views=1, visit_date=time.strftime(
            '%Y-%m-%d', time.localtime(time.time())))
    else:
        postview.views += 1
    history = History(ip=request.remote_addr, post_id=id, platform=request.user_agent.platform,
                      browser=request.user_agent.browser, visit_time=datetime.now())
    db.session.add(history)
    db.session.add(postview)
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
    return render_template('post.html', current_user=current_user, post=post, comments=comments, form=form, pagination=pagination, title=title)


@main.route("/timeline")
def timeline():
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.order_by(Post.create_at.desc()).paginate(
        page, per_page=current_app.config['FLASK_PER_PAGE'], error_out=True)
    posts = pagination.items
    post_dict = group_posts_by_date(posts)
    return render_template("timeline.html", current_user=current_user, post_dict=post_dict, pagination=pagination)


def group_posts_by_date(posts):
    post_dict = OrderedDict()
    for post in posts:
        year_month = post.create_at.strftime("%Y-%m")
        if post_dict.get(year_month, None) is None:
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
        return render_template("search.html", posts=posts, keyword=keyword)
    else:
        abort(404)


@main.route("/about", methods=["GET", "POST"])
def about():
    form = CommentForm()
    if form.validate_on_submit():
        platform = request.user_agent.platform
        browser = request.user_agent.browser
        message_board = MessageBoard(message_type=0, user_name=form.user_name.data, email=form.email.data, website=form.website.data,
                                     message=form.comment.data, platform=platform, browser=browser, message_time=datetime.now())
        db.session.add(message_board)
        try:
            db.session.commit()
            flash("留言成功!")
        except Exception as e:
            db.session.rollback()
        
        return redirect(url_for("main.about"))
    page = request.args.get('page', 1, type=int)
    pagination = MessageBoard.query.filter_by(message_type=0).order_by(MessageBoard.message_time.desc(
    )).paginate(page, per_page=current_app.config['FLASK_PER_PAGE'], error_out=True)
    comments = pagination.items
    return render_template("about.html", current_user=current_user, comments=comments, pagination=pagination, form=form)


@main.route("/friends", methods=["POST", "GET"])
def friend_links():
    form = CommentForm()
    if form.validate_on_submit():
        platform = request.user_agent.platform
        browser = request.user_agent.browser
        message_board = MessageBoard(message_type=1, user_name=form.user_name.data, email=form.email.data, website=form.website.data,
                                     message=form.comment.data, platform=platform, browser=browser, message_time=datetime.now())
        db.session.add(message_board)
        db.session.commit()
        flash("留言成功!")
        return redirect(url_for("main.about"))
    page = request.args.get('page', 1, type=int)
    pagination = MessageBoard.query.filter_by(message_type=1).order_by(MessageBoard.message_time.desc(
    )).paginate(page, per_page=current_app.config['FLASK_PER_PAGE'], error_out=True)
    comments = pagination.items
    friend_links = FriendLink.query.all()
    return render_template("friend_links.html", current_user=current_user, comments=comments, friend_links=friend_links, pagination=pagination, form=form)


def get_abs_url(title):
    url = "post/{}".format(title)
    return urljoin(request.url_root, url)


@main.route("/feeds")
def feeds():
    feeds = AtomFeed(title="Peach Blog's Feeds",
                     feed_url=request.url, url=request.url_root)
    posts = Post.query.order_by(Post.create_at.desc()).all()
    for post in posts:
        feeds.add(post.title, markdown.html(post.content), content_type='html', author='Leetao',
                  url=get_abs_url(post.title), updated=post.last_update, published=post.last_update)
    return feeds.get_response()
