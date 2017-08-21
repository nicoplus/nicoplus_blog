from app.models import Permissions

from functools import wraps

from flask_login import current_user
from flask import abort


def permission_required(permission):
    def decorator(f):
        @wraps(f)
        def decorator_func(*args, **kws):
            if not current_user.can(permission):
                abort(403)
            return f(*args, **kws)
        return decorator_func
    return decorator


def admin_required(f):
    return permission_required(Permissions.ADMIN)(f)
