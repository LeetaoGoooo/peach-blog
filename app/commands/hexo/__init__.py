from __future__ import print_function
import sys
import errno
import os
import glob
from functools import wraps
from flask import current_app
from flask.cli import AppGroup
from app.models import Post, Tag
import markdown
from datetime import datetime
import logging
import json
import re

log = logging.getLogger()

class Hexo:

    def __init__(self, app = None, db = None, directory='posts'):
        self.db = db
        self.directory = directory
        self.md = markdown.Markdown(extensions = ['meta'])
        
        if app is not None and db is not None:
            self.init_app(app, db, directory)

    def init_app(self, app, db=None, directory=None, **kwargs):
        self.db = db or self.db
        self.directory = directory or self.directory
        
        base_path = os.path.dirname(app.instance_path)
        self.directory = os.path.join(base_path,self.directory)

        if not os.path.exists(self.directory):
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), self.directory)

        self.version_json_path = os.path.join(self.directory,'version.json')
        
        if not hasattr(app, 'extensions'):
            app.extensions = {}
        app.extensions['hexo'] = self
    
    def get_post_file_modify_dict(self):
        path = os.path.join(self.directory,'*.md')
        post_file_modify_dict = {}
        for file_name in glob.glob(path):
            post_file_modify_dict[os.path.basename(file_name)] = os.path.getmtime(file_name)
        return post_file_modify_dict

    def get_post_file_version_dict(self):
        post_file_version_dict = {}
        if os.path.exists(self.version_json_path):
            with open(self.version_json_path,'r', encoding='utf-8') as f:
                post_file_version_dict = json.load(f)
        return post_file_version_dict

    def get_generate_file_list(self):
        generate_file_list = []

        new_version_dict = {}

        post_file_modify_dict = self.get_post_file_modify_dict()
        post_file_version_dict = self.get_post_file_version_dict()

        for file_name,last_modify_time in post_file_modify_dict.items():
            order_last_modify_time = post_file_version_dict.get(file_name, None)
            if order_last_modify_time != last_modify_time:
                generate_file_list.append(file_name)

        with open(self.version_json_path, 'w') as f:
            json.dump(post_file_modify_dict,f)

        return generate_file_list

    def get_post_detail_dict(self, file_name):
        path = os.path.join(self.directory, file_name)
        with open(path,'r',encoding='utf-8') as f:
            content =  f.read()
            html = self.md.convert(content)
            meta = self.md.Meta
            create_at = meta.get("date",None)
            if create_at is not None:
                create_at = create_at[0]
            content = Hexo.get_post_content_without_meta(content)
            return {"title": meta['title'][0], "tag_list": meta['tag'][0][1:-1].split(","), "content": content, "create_at" : create_at} 

    def update_or_insert_post(self, post_detail_dict):
        
        tag_list = post_detail_dict.get("tag_list")
        title = post_detail_dict.get("title")
        content = post_detail_dict.get("content")
        create_at = post_detail_dict.get("create_at")

        print("generate post {} ...".format(title))

        all_tag_list = []
        for tag_name in tag_list:
            tag = Tag.query.filter_by(tag=tag_name).first()
            if tag is None:
                tag = Tag(tag=tag_name)
            all_tag_list.append(tag)
        post = Post.query.filter_by(title=title).first()
        if post is None:
            post = Post(title=title, content=content, create_at= datetime.strptime(create_at, "%Y-%m-%d"))
        else:
            post.content = content
            post.create_at = create_at= datetime.strptime(create_at, "%Y-%m-%d")
        post.tags.extend(all_tag_list)
        self.db.session.add(post)
        self.db.session.commit()

    def generate_posts(self):
        """
         generate posts into database
        """
        generate_file_list = self.get_generate_file_list()
        for file_name in generate_file_list:
            post_detail_dict = self.get_post_detail_dict(file_name)
            self.update_or_insert_post(post_detail_dict)
        print("generate posts successfully!")
    
    def clean_posts(self):
        """
            clean posts and post2tag
        """
        post_file_version_dict = self.get_post_file_version_dict()

        try:
            posts = Post.query.all()
            for post in posts:
                post.tags.clear()
            num_post_rows_deleted = self.db.session.query(Post).delete()
            self.db.session.commit()
            print("{} posts have already been deleted".format(num_post_rows_deleted))
            if os.path.exists(self.version_json_path):
                os.remove(self.version_json_path)
        except Exception as e:
            print(e)
            self.db.session.rollback()
            with open(self.version_json_path, 'w') as f:
                json.dump(post_file_version_dict,f)
            

    def export_posts(self):
        """
         export markdown post to directory 
        """
        pass

    @staticmethod
    def get_post_content_without_meta(content):
        pattern = re.compile(r"\s*---.+---(.+)", re.MULTILINE|re.DOTALL)
        matches = re.match(pattern, content)
        print(matches)
        if matches is not None:
            return matches.group(1)
        return matches

    @property
    def metadata(self):
        return self.db.metadata

def catch_errors(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        try:
            f(*args, **kwargs)
        except RuntimeError as exc:
            log.error('Error: ' + str(exc))
            sys.exit(1)
    return wrapped


@catch_errors
def generate():
    current_app.extensions['hexo'].generate_posts()

@catch_errors
def clean():
    current_app.extensions['hexo'].clean_posts()

@catch_errors
def export(directory = None):
    pass