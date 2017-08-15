from flask_migrate import Migrate

from app import create_app
from app.extension import db
from app import models
#必须引入models，否则flask-migrate无法检测到模型的变动

import os

app = create_app(os.environ.get('FLASK_CONFIG') or 'default')
migrate = Migrate(app, db)


@app.shell_context_processor
def make_shell_context():
    return dict(app=app, db=db, models=models)
