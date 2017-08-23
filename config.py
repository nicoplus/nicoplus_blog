import os

base_dir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    FLASK_ADMIN = os.environ.get('FLASK_ADMIN', None)
    FLASK_MAIL_SUBJECT_PREFIX = '[Nicoplus Blog]'
    FLASK_MAIL_SENDER = 'nicoplus@qq.com'
    UPLOADED_PHOTOS_DEST = '/var/www/flask_blog/'
    FLASK_POSTS_PER_PAGE = 20

    CELERY_BROKER_URL = 'redis://localhost:6379/0'
    CELERY_ACCEPT_CONTENT = ['json', 'msgpack', 'pickle']

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://nicoplus:jc1992@localhost/blogdev'
    MAIL_SERVER = 'smtp.qq.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or 'nicoplus@qq.com'
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or 'vjnlmcjpzisabibf'


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://nicoplus:jc1992@localhost/blogtest'


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'postgresql://nicoplus:jc1992@localhost/blog'  # 未创建


config = {
    'development': DevelopmentConfig,
    'testing': TestConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
