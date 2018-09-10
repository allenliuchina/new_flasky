from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from config import config
from flask_login import LoginManager
from flask_mail import Mail
from flask_pagedown import PageDown
import flask_whooshalchemyplus
import memcache

mail = Mail()
bootstrap = Bootstrap()
moment = Moment()
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.session_protection = 'basic'
pagedown = PageDown()
mc = memcache.Client(['127.0.0.1:11211'], debug=True)


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    bootstrap.init_app(app)
    db.init_app(app)
    moment.init_app(app)
    mail.init_app(app)
    login_manager.init_app(app)
    pagedown.init_app(app)
    flask_whooshalchemyplus.init_app(app)
    from .main import main
    app.register_blueprint(main)
    from .auth import auth
    app.register_blueprint(auth)
    from .api_1_0 import api as api_1_0
    app.register_blueprint(api_1_0, url_prefix='/api/v1.0')
    return app
