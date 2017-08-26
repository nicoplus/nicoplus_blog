from . import main
from app.extension import db
from app.models import Permissions

from flask_sqlalchemy import get_debug_queries
from flask import current_app


@main.after_app_request
def session_commit(resp, *args, **kws):
    db.session.commit()
    return resp


@main.after_app_request
def slow_query(resp, *args, **kws):
    for query in get_debug_queries():
        if query.duration >= current_app.config['DATABASE_QUERY_TIMEOUT']:
            current_app.logger.warn(
                'Context:{}\nSLOW QUERY: {}\nParameters: {}\n'
                'Duration: {}\n'.format(
                    query.context, query.statement,
                    query.parameters, query.duration))
    return resp


@main.teardown_app_request
def session_remove(exception=None):
    try:
        db.session.remove()
    except Exception as e:
        print(e)
    finally:
        pass


@main.app_template_filter('post_datetime')
def post_datetime(datetime):
    return datetime.strftime('%Y-%m-%d %H:%M')


@main.app_context_processor
def inject_permissions():
    return dict(Permissions=Permissions)
