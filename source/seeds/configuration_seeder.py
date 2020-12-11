
from flask_seeder import Seeder

from app.models.configuration import Configuration


class ConfigurationSeeder(Seeder):

    def __init__(self, db=None):
        super().__init__(db=db)
        self.priority = 1

    def run(self):
        print("[ConfigurationSeeder]")
        Configuration().save()
        print(f" - Configuration OK")
