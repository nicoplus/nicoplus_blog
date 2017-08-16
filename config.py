import os

base_dir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://nicoplus:jc1992@localhost/blogdev'


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://nicoplus:jc1992@localhost/blogtest'


class ProductionConfig(Config):
    FLASK_ADMIN = os.environ.get('FLASK_ADMIN')#运行时，需在虚拟环境activate脚本中写入
    SQLALCHEMY_DATABASE_URI = 'postgresql://nicoplus:jc1992@localhost/blog'# 未创建


config = {
    'development': DevelopmentConfig,
    'testing': TestConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
