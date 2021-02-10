from flask import session


def add_alert(alert, name="alert"):
    """Add an alert message to in the session

    Parameters:
    alert (string): message to be stored in the session
    name (string): key used to access the message

   """
    session[name] = alert


def get_alert(name="alert"):
    """Returns a message stored in the session

    Parameters:
    name (string): key used to access the message

    Returns:
    string:Return a message

   """
    alert = session.get(name, None)
    if alert:
        session.pop(name)
    return alert
