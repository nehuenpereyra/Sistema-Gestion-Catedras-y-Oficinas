from flask import Flask
import unittest
from flask_sqlalchemy import SQLAlchemy
from app import delete_app, set_db
from config.config import config


class BaseTestClass(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.config.from_object(config["unittest"])
        set_db(self.app)
    
    def tearDown(self):
        delete_app(self.app)

    
        