import sys
import errno
import os
import glob
from functools import wraps
from flask import current_app
import logging
import json

log = logging.getLogger()

class Hexo:

    def __init__(self, app = None, db = None, directory='posts'):
        self.db = db
        self.directory = directory
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
        version_json_path = os.path.join(self.directory,'version.json')
        post_file_version_dict = {}
        if os.path.exists(version_json_path):
            with open(version_json_path,'r', encoding='utf-8'):
                post_file_version_dict = json.load(f)
                return post_file_version_dict
        return post_file_version_dict

    def get_unstored_post_list(self):
        pass


    def generate_posts(self):
        """
         generate posts into database
        """
        pass
    
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


@catch_errors
def generate():
    pass

@catch_errors
def export(directory = None):
    pass