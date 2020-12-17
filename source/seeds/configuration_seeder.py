
from flask_seeder import Seeder

from app.models.configuration import Configuration


class ConfigurationSeeder(Seeder):

    def __init__(self, db=None):
        super().__init__(db=db)
        self.priority = 1

    def run(self):
        print("[ConfigurationSeeder]")
        Configuration(mail_contact="admin@admin.com", items_per_page=10, mail_server="admin@admin.com", mail_port=666, mail_password="admin123").save()
        print(f" - Configuration OK")
