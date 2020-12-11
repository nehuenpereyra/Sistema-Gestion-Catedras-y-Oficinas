from flask import session


def add_alert(alert, name="alert"):
    session[name] = alert


def get_alert(name="alert"):
    alert = session.get(name, None)
    if alert:
        session.pop(name)
    return alert
