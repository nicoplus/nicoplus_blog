from flask_migrate import Migrate
from flask.cli import with_appcontext
try:
    import IPython
    has_ipython = True
except:
    has_ipython = False

from app import create_app
from app.extension import db
from app import models
# 必须引入models，否则flask-migrate无法检测到模型的变动

import os
import sys
import code
import click


app = create_app(os.environ.get('FLASK_CONFIG') or 'default')
migrate = Migrate(app, db)


@app.shell_context_processor
def make_shell_context():
    return dict(app=app, db=db, models=models)


def plain_shell(user_ns, banner):
    sys.exit(code.interact(banner=banner, local=user_ns))


def ipython_shell(user_ns, banner):
    IPython.embed(banner1=banner, user_ns=user_ns)


@app.cli.command('new_shell', short_help='Runs a shell in the app context.')
@click.option('--plain', help='Use Plain Shell', is_flag=True)
@with_appcontext
def shell_command(plain):
    from flask.globals import _app_ctx_stack
    app = _app_ctx_stack.top.app
    banner = 'Python %s on %s\nApp: %s%s\nInstance: %s' % (
        sys.version,
        sys.platform,
        app.import_name,
        app.debug and '[debug]' or '',
        app.instance_path,)
    user_ns = app.make_shell_context()
    use_palin_shell = not has_ipython or plain
    if use_palin_shell:
        plain_shell(user_ns, banner)
    else:
        ipython_shell(user_ns, banner)
