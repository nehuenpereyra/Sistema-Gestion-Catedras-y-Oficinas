
from flask import abort
from flask_login import current_user

from app.models import Permission


def verify_permission(permission, id=None):
    """Check if the currently logged in user has the permissions """
    return current_user.has_permission_for(permission, id)


def permission(name):
    """Decorator that verifies if the currently logged in user has the permissions to perform an operation.
    If you don't have the permissions, perform an abort (403).

    Parameters:
    name (string): representing permission

    Returns:
    function:Return a function

    """
    def wrapper_1(function):
        def wrapper_2(*args, **kwargs):
            if not current_user.is_authenticated:
                abort(401)
            if not verify_permission(name, kwargs.get("id", None)):
                abort(403)
            return function(*args, **kwargs)
        return wrapper_2
    return wrapper_1
