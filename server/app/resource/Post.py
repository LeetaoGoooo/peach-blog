from flask_restful import Resource, reqparse
from flask import jsonify, current_app
from flask_jwt_extended import jwt_required
from app.models import Post
from app import db


class PostListResource(Resource):

    def __init__(self):
        total_post_count = Post.query.count()
        remain_flag = total_post_count %  current_app.config['FLASKY_POSTS_PER_PAGE'] 
        if remain_flag:
            self.total_page = total_post_count // current_app.config['FLASKY_POSTS_PER_PAGE'] + 1
        else:
            self.total_page = total_post_count // current_app.config['FLASKY_POSTS_PER_PAGE']


    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('page', type=int, location='args')
        args = parser.parse_args()
        page = args['page']
        if page is None:
            page = 1
        posts = Post.query.order_by(Post.create_at.desc()).offset(page * current_app.config['FLASKY_POSTS_PER_PAGE'] + 1).limit(current_app.config['FLASKY_POSTS_PER_PAGE'])
        post_json_list = [post.json for post in posts]
        return {"total_page":self.total_page,"current_page":page,"posts":post_json_list}



class PostResource(Resource):

    def get(self, title):
        post = Post.query.filter_by(title=title).first()
        return post.json

    def post(self):
        parse = reqparse.RequestParser()
        parse.add_argument('post')
        args = parser.parse_args()
        post_dict = args['post']
        post = Post(title=post_dict['title'],content=post_dict['content'])
        db.session.add(post)
        db.sessin.commit()
        post = Post.query.filter_by(title=post_dict['title']).first()
        return post.json


    def put(self, post):
        pass

    def delete(self, title):
        pass
