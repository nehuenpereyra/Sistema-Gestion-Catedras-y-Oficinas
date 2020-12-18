from flask import session


def add_previous_path(path, name="path"):
    session[name] = path


def get_previous_path(name="path"):
    path = session.get(name, None)
    if path:
        session.pop(name)
    return path
