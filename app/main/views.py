from flask import render_template, redirect, url_for, flash
from flask_login import current_user
from app.models import Tag

@main.route("/", methods=['GET'])
def index():
    pass
