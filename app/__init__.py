import os

from flask import Flask
from celery import Celery

from app.extension import bootstrap, toolbar, db, pagedown,\
    login_manager, mail, photos, configure_uploads, admin
from config import config
from app.utils import create_slow_query_handler


def create_app(config_name=None):
    '''传入配置名：
            'development'
            'testing'
            'production'
            'default'(development模式)
            如若为None则为default
            '''
    config_name = config_name or 'default'
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    toolbar.init_app(app)
    db.init_app(app)
    pagedown.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    configure_uploads(app, photos)

    create_slow_query_handler(app)

    from . import admin_view
    if admin.app is None:
        admin.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    return app


def create_celery_app(app=None):
    app = app or create_app(config_name=os.environ.get('FLASK_CONFIG'))
    celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return super(TaskBase, self).__call__(*args, **kwargs)

    celery.Task = ContextTask
    return celery



