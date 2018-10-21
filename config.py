import os


class Config():
    SECRET_KEY = 'DJFLDSFJKDSJFJ'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True  # 改成False 就不能发送信号，whoosh不能自动增加索引
    FLASKY_ADMIN = '15603363510@163.com'
    SQLALCHEMY_RECORD_QUERIES = True
    FLASKY_SLOW_DB_QUERY_TIME = 0.5
    # UPLOAD_FOLDER = '/home/lya/doc/new_flasky/instances'
    UPLOAD_FOLDER = os.path.join(os.path.abspath(os.path.dirname(__name__)), 'app', 'static')
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.163.com')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', '25'))
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() in \
                   ['true', 'on', 'email']
    MAIL_USERNAME = '15603363510'
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    FLASKY_MAIL_SUBJECT_PREFIX = '[Flasky]'
    FLASKY_MAIL_SENDER = 'Flasky Admin <15603363510@163.com>'


class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:root@127.0.0.1/test'
    #    SQLALCHEMY_DATABASE_URI = 'sqlite:////home/lya/doc/new_flasky/test.sqlite'
    TESTING = True
    WTF_CSRF_ENABLED = False


class DevConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:root@127.0.0.1/dev'
    DEBUG = True
    TEMPLATES_AUTO_RELOAD = True


class ProdConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:root@127.0.0.1/prod'


config = {
    'dev': DevConfig,
    'test': TestConfig,
    'prod': ProdConfig,
}
