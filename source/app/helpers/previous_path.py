from flask import session


def add_previous_path(path, name="path"):
    """Add the path sent by parameter to the session

    Parameters:
    path (string): path to be stored in the session
    name (string): key used to access the message

   """
    session[name] = path


def get_previous_path(name="path"):
    """Returns a path stored in the session

    Parameters:
    name (string): key used to access to path

    Returns:
    string:Return a path

   """
    path = session.get(name, None)
    if path:
        session.pop(name)
    return path
