from flask_restful import Resource, reqparse, abort,marshal_with
from flask import jsonify, current_app
from flask_jwt_extended import jwt_required
from app.models import Post
from app import db
import datetime
from .Field import PostField,PostListField

class PostListResource(Resource):

    def __init__(self):
        total_post_count = Post.query.count()
        remain_flag = total_post_count %  current_app.config['FLASKY_POSTS_PER_PAGE'] 
        if remain_flag:
            self.total_page = total_post_count // current_app.config['FLASKY_POSTS_PER_PAGE'] + 1
        else:
            self.total_page = total_post_count // current_app.config['FLASKY_POSTS_PER_PAGE']


    @marshal_with(PostListField)
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('page', type=int, location='args')
        args = parser.parse_args()
        page = args['page']
        if page is None:
            page = 1
        posts = Post.query.order_by(Post.create_at.desc()).offset(page * current_app.config['FLASKY_POSTS_PER_PAGE'] + 1).limit(current_app.config['FLASKY_POSTS_PER_PAGE'])
        data = {"total_page": self.total_page, "current_page": page, "posts":posts}
        return data


class PostResource(Resource):

    @marshal_with(PostField)
    def get(self, title):
        post = Post.query.filter_by(title=title).first()
        if post is None:
            abort(404, message = "Post {} doesn't exist".format(title)) 
        return post

    @marshal_with(PostField)
    def post(self, title):
        parse = reqparse.RequestParser()
        parse.add_argument('title')
        parse.add_argument('content')
        args = parse.parse_args()
        post = Post(title=args['title'],content=args['content'])
        db.session.add(post)
        db.session.commit()
        post = Post.query.filter_by(title=args['title']).first()
        return post

    @marshal_with(PostField)
    def put(self, title):
        parse = reqparse.RequestParser()
        parse.add_argument('title')
        parse.add_argument('content')
        args = parser.parse_args()        
        post = Post(title=args['title'],content=args['content'])
        db.session.add(post)
        db.session.commit()
        return post

    @jwt_required
    def delete(self, title):
        post = Post.query.filter_by(title=title).first()
        db.session.delete(post)
        db.session.commit()
        return {"status":True,"msg":"删除成功!"}
