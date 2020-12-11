from flask_login import LoginManager, current_user
from app.models.user import User

login_manager = LoginManager()

def set_login(app):
    login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(user_id)

def authenticated():
    return current_user.is_active
