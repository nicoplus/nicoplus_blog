from app.extension import mail

from flask_mail import Message
from flask import render_template, current_app


def send_email(to, subjct, template, **kw):
    #app = current_app._get_current_object()
    msg = Message(current_app.config['FLASK_MAIL_SUBJECT_PREFIX'] + subjct,
                  sender=current_app.config['FLASK_MAIL_SENDER'], recipients=[to])
    msg.body = render_template(template + '.txt', **kw)
    msg.html = render_template(template + '.html', **kw)
    mail.send(msg)
