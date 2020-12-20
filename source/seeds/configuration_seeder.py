
from flask_seeder import Seeder

from app.models.configuration import Configuration


class ConfigurationSeeder(Seeder):

    def __init__(self, db=None):
        super().__init__(db=db)
        self.priority = 1

    def run(self):
        print("[ConfigurationSeeder]")
        Configuration(mail_contact="admin@admin.com", items_per_page=10,
                      mail_server="smtp.gmail.com", mail_port=465, mail_password="password").save()
        print(f" - Configuration OK")
