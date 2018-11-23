from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_misaka import Misaka
from config import config
from utils import Tools

bootstrap = Bootstrap()
db = SQLAlchemy()
migrate = Migrate()
misaka = Misaka()
tools = Tools()

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'
login_manager.login_message = '请登录后访问该页面'

from .commands.hexo import Hexo
hexo = Hexo()

from admin import PeachAdmin
admin = PeachAdmin(name="PeachBlog", template_mode="bootstrap3")


def create_app(config_name):
    app = Flask(__name__, static_folder='static', static_url_path='')

    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    misaka.init_app(app)
    db.init_app(app)
    # migrate 生效，确保 model 被引入
    migrate.init_app(app, db)
    hexo.init_app(app, db)
    admin.init_app(app, db)
    tools.init_app(app)
    login_manager.init_app(app)

    from .commands.hexo.cli import hexo_cli

    app.cli.add_command(hexo_cli)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    from .api_v1_0 import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api/v1')

    return app
