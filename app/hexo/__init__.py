import sys
from functools import wraps
from flask import current_app
import logging

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
        if not hasattr(app, 'extensions'):
            app.extensions = {}
        app.extensions['hexo'] = self
    
    def generate(self):
        """
         generate posts into database
        """
        pass
    
    def export(self):
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