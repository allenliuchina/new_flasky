class Config():
    SECRET_KEY = 'DJFLDSFJKDSJFJ'
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:root@127.0.0.1/test'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True


config = {
    'dev': Config,
}
