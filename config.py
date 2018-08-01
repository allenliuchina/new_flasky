class Config():
    SECRET_KEY = 'DJFLDSFJKDSJFJ'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True


class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:root@127.0.0.1/test'
#    SQLALCHEMY_DATABASE_URI = 'sqlite:////home/lya/doc/new_flasky/test.sqlite'
    TESTING=True

class DevConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:root@127.0.0.1/dev'


config = {
    'dev': DevConfig,
    'test': TestConfig,
}
