import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
from flask import current_app
from . import main
import os

mail_handler = SMTPHandler(
    mailhost=('smtp.163.com', '465'),
    fromaddr='15603363510@163.com',
    toaddrs=['772075034@qq.com'],
    subject='Application Error',
    credentials=('15603363510', os.environ.get('MAIL_PASSWORD'))
)
mail_handler.setLevel(logging.ERROR)
mail_handler.setFormatter(logging.Formatter(
    '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
))

txt_handler = RotatingFileHandler('log.txt')
txt_handler.setLevel(logging.INFO)
txt_handler.setFormatter(logging.Formatter(
    '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
))


@main.before_app_first_request
def fun():
    app = current_app._get_current_object()
    if not app.debug:
        app.logger.addHandler(mail_handler)
        app.logger.addHandler(txt_handler)
