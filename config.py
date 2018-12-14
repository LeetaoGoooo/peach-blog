import logging
import os

basedir = os.path.abspath(os.path.dirname(__file__))


class InfoFilter(logging.Filter):
    def filter(self, record):
        if logging.INFO <= record.levelno < logging.ERROR:
            return super().filter(record)
        else:
            return 0


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True
    FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN')
    FLASK_PER_PAGE = 20
    FLASKY_POSTS_PER_PAGE = 10
    FLASKY_COMMENTS_PER_PAGE = 30
    EXPORT_POST_DIRECTORY = os.path.join(basedir, 'posts')

    LOG_PATH = os.path.join(basedir, 'logs')
    LOG_PATH_ERROR = os.path.join(LOG_PATH, 'error.log')
    LOG_PATH_INFO = os.path.join(LOG_PATH, 'info.log')
    LOG_FILE_MAX_BYTES = 100 * 1024 * 1024
    LOG_FILE_BACKUP_COUNT = 10

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    FLASK_ENV = 'development'
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DEV_DATABASE_URL') or 'mysql+pymysql://root:@localhost:3306/peach_blog_dev?charset=utf8'

    @classmethod
    def init_app(self, app):
        Config.init_app(app)
        import logging
        from logging.handlers import RotatingFileHandler

        # Formatter
        formatter = logging.Formatter(
            '%(asctime)s %(levelname)s %(process)d %(thread)d '
            '%(pathname)s %(lineno)s %(message)s')

        # FileHandler Info
        file_handler_info = RotatingFileHandler(filename=self.LOG_PATH_INFO)
        file_handler_info.setFormatter(formatter)
        file_handler_info.setLevel(logging.INFO)
        info_filter = InfoFilter()
        file_handler_info.addFilter(info_filter)
        app.logger.addHandler(file_handler_info)

        # FileHandler Error
        file_handler_error = RotatingFileHandler(filename=self.LOG_PATH_ERROR)
        file_handler_error.setFormatter(formatter)
        file_handler_error.setLevel(logging.ERROR)
        app.logger.addHandler(file_handler_error)


class TestingConfig(Config):
    ENV = 'testing'
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DEV_DATABASE_URL') or 'mysql+pymysql://root:@localhost:3306/peach_blog_test?charset=utf8'


class ProductionConfig(Config):
    ENV = 'production'
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DEV_DATABASE_URL') or 'mysql+pymysql://root:@localhost:3306/peach_blog?charset=utf8'

    @classmethod
    def init_app(self, app):
        Config.init_app(app)
        import logging
        from logging.handlers import RotatingFileHandler

        # Formatter
        formatter = logging.Formatter(
            '%(asctime)s %(levelname)s %(process)d %(thread)d '
            '%(pathname)s %(lineno)s %(message)s')

        # FileHandler Info
        file_handler_info = RotatingFileHandler(filename=self.LOG_PATH_INFO)
        file_handler_info.setFormatter(formatter)
        file_handler_info.setLevel(logging.INFO)
        info_filter = InfoFilter()
        file_handler_info.addFilter(info_filter)
        app.logger.addHandler(file_handler_info)

        # FileHandler Error
        file_handler_error = RotatingFileHandler(filename=self.LOG_PATH_ERROR)
        file_handler_error.setFormatter(formatter)
        file_handler_error.setLevel(logging.ERROR)
        app.logger.addHandler(file_handler_error)



config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
