from os import environ
from flask import current_app
from flask_mail import Mail, Message

from .configuration import Configuration

class MailSender():

    @staticmethod
    def get_mail():
        current_app.config['MAIL_SERVER']= Configuration.get().mail_server
        current_app.config['MAIL_PORT'] = Configuration.get().mail_port
        current_app.config['MAIL_USERNAME'] = environ.get("MAIL_USERNAME", Configuration.get().mail_contact)
        current_app.config['MAIL_PASSWORD'] = environ.get("MAIL_PASSWORD", Configuration.get().mail_password)
        current_app.config['MAIL_USE_TLS'] = False
        current_app.config['MAIL_USE_SSL'] = True
        return Mail(current_app)
        
    @staticmethod
    def send_to_user(title, message, email):
        mail = MailSender.get_mail()
        msg = Message(title, sender = current_app.config['MAIL_USERNAME'], recipients = [email], body=message)
        mail.send(msg)

    @staticmethod
    def send(title, messagee):
        mail = MailSender.get_mail()
        msg = Message(title , sender = current_app.config['MAIL_USERNAME'], recipients = [current_app.config['MAIL_USERNAME']], body=messagee)
        mail.send(msg)
    