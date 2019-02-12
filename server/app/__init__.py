from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restful import Resource, Api
from config import config

db = SQLAlchemy()
migrate = Migrate()
api = Api()

from .commands.hexo import Hexo
hexo = Hexo()

def create_app(config_name):
    app = Flask(__name__, static_folder='static', static_url_path='')

    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    db.init_app(app)
    migrate.init_app(app, db)
    hexo.init_app(app, db)
    api.init_app(app)

    from .commands.hexo.cli import hexo_cli

    app.cli.add_command(hexo_cli)

    from .api_v1_0 import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api/v1')

    return app
