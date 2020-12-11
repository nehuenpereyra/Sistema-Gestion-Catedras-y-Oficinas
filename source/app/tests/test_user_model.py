from . import BaseTestClass 
from app.resources.user import User
from werkzeug.security import generate_password_hash

class UserModelTest(BaseTestClass):

    def test_user_new(self):
        with self.app.app_context():
            UserModelTest.create_user("test@test.com","test","test","test","123123").save()
            result = User.find_by_email("test@test.com").get_email
        self.assertEqual("test@test.com",result)

    @staticmethod
    def create_user(email, username, first_name, last_name, password):
        return User(username= username ,email=email, 
        first_name=first_name, last_name=last_name,
        password=generate_password_hash(password))