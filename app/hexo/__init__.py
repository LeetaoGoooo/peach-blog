import sys
import errno
import os
import glob
from functools import wraps
from flask import current_app
from flask.cli import AppGroup
from app.models import Post, Tag, Post2Tag
from app import db
import markdown
from datetime import datetime
import logging
import json



log = logging.getLogger()

class Hexo:

    def __init__(self, app = None, db = None, directory='posts'):
        self.db = db
        self.directory = directory
        self.version_json_path = os.path.join(self.directory,'version.json')
        self.md = markdown.Markdown(extensions = ['meta'])
        
        if app is not None and db is not None:
            self.init_app(app, db, directory)

    def init_app(self, app, db=None, directory=None, **kwargs):
        self.db = db or self.db
        self.directory = directory or self.directory
        
        if os.path.exists(self.directory):
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), self.directory)

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
            with open(self.version_json_path,'r', encoding='utf-8'):
                post_file_version_dict = json.load(f)
                return post_file_version_dict
        return post_file_version_dict

    def get_generate_file_list(self):
        generate_file_list = []

        new_version_dict = {}

        post_file_modify_dict = self.get_post_file_modify_dict()
        post_file_version_dict = self.get_post_file_version_dict()

        for file_name,last_modify_time in post_file_modify_dict:
            order_last_modify_time = post_file_version_dict.get(file_name, None)
            if order_last_modify_time != last_modify_time:
                generate_file_list.append(file_name)

        with open(self.version_json_path, 'r') as f:
            json.dump(post_file_modify_dict,f)

        return generate_file_list

    def get_post_detail_dict(self, file_name):
        path = os.path.join(self.directory, file_name)
        with open(path,'r',encoding='utf-8') as f:
            content =  r.read()
            html = self.md.convert(text)
            meta = md.Meta
            create_at = meta.get("date",None)
            if create_at is not None:
                create_at = create_at[0]
            return {"title": meta['title'][0], "tag_list": meta['tag'][0], "content": content, "create_at" : create_at} 

    def update_or_insert_post(**kw):
        tag_list = kw.get("tag_list")
        title = kw.get("title")
        content = kw.get("content")
        create_at = kw.get("create_at")

        all_tag_list = []
        for tag in tag_list:
            tag = Tag.query.filter_by(tag=tag).first()
            if tag is None:
                tag = Tag(tag=tag)
            all_tag_list.append(tag)

        post = Post.query.filter_by(title=kw.get("title")).first()
        if post is None:
            post = Post(title=title, content=content, create_at= datetime.strptime(create_at, "%Y-%m-%d"))
        else:
            post.content = content
            post.create_at = create_at= datetime.strptime(create_at, "%Y-%m-%d")
        post.post2map.extend(all_tag_list)
        db.session.add(post)
        db.session.add(all_tag_list)
        db.session.commit()

    def generate_posts(self):
        """
         generate posts into database
        """
        generate_file_list = self.get_generate_file_list()
        for file_name in generate_file_list:
            self.update_or_insert_post(self.get_post_detail_dict(file_name))
        print("generate posts successfully!")
    
    
    def export_posts(self):
        """
         export markdown post to directory 
        """
        pass

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


hexo_cli = AppGroup('hexo')

@hexo_cli.command("g")
@catch_errors
def generate():
    current_app.extensions['hexo'].generate_posts()

@catch_errors
def export(directory = None):
    pass

current_app.cli.add_command(hexo_cli)