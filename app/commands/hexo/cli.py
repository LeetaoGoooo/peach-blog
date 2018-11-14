import click
from flask import current_app
from flask.cli import AppGroup, with_appcontext
from . import generate as _generate
from . import clean as _clean

hexo_cli = AppGroup("hexo")

@hexo_cli.command("g")
@with_appcontext
def generate():
    """Creates a new migration repository."""
    _generate()

@hexo_cli.command("c")
@with_appcontext
def clean():
    """Clean all posts in database"""
    _clean()