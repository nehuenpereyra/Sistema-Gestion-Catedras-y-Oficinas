from flask_login import LoginManager, current_user
from app.models import User

login_manager = LoginManager()


def set_login(app):
    login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    """Returns a user with the id sent by argument

    Parameters:
    user_id (int): user id

    Returns:
    User:Return a user

   """
    return User.get(user_id)


def authenticated():
    """Returns if the user is authenticated """
    return current_user.is_active
