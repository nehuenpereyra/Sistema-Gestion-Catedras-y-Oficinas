from sqlalchemy import event

from app.db import db


class Configuration(db.Model):

    __tablename__ = 'configuration'

    id = db.Column(db.Integer, primary_key=True)
    mail_contact = db.Column(
        db.String(30), unique=True, nullable=False, default="")
    items_per_page = db.Column(db.Integer, nullable=False, default=10)
    mail_server = db.Column(db.String(160), nullable=False, default="")
    mail_port = db.Column(db.Integer, nullable=False, default=465)
    mail_password = db.Column(db.String(128), nullable=False, unique=False)

    def __repr__(self):
        return f'<Configuration {self.title}>'

    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()

    @staticmethod
    def get():
        return Configuration.query.first()

    @staticmethod
    def update(mail_server, mail_port, contact_email, items_per_page, mail_password):
        config = Configuration.get()
        config.mail_server = mail_server
        config.mail_port = mail_port
        config.mail_contact = contact_email
        config.items_per_page = items_per_page
        config.mail_password = mail_password
        config.save()
