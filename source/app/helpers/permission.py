from flask import abort
from flask_login import current_user

def verify_permission(permission):
    return current_user.roles.flat_collect(lambda each: each.permissions).any_satisfy(lambda each: each.name == permission)

def permission(name):
    def wrapper_1(function):
        def wrapper_2(*args, **kwargs):
            if not current_user.is_authenticated:
                abort(401)
            if not verify_permission(name):
                abort(403)
            return function(*args, **kwargs)
        return wrapper_2
    return wrapper_1
