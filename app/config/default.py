# coding=utf-8
'''配置模块'''


class Config(object):
    '''
    默认配置数据
    '''

    # Flask config
    DEBUG = False
    TESTING = False
    SECRET_KEY = '‭1DF5E76‬'
    JSON_AS_ASCII = False

    # mongodb config
    # ex: mongodb://root:aaa2016@localhost:27017/mongo_test
    # MONGO_URI = os.environ.get('APP_MONGO_URI')

    # Mysql
    SQLALCHEMY_DATABASE_URI = 'mysql://user:Password@localhost/instance'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True

    # redis
    # REDIS_URL = "redis://:password@localhost:6379/0"

    # App config
    APP_SERVICE_NAME = 'micelle'
    APP_LOG_LEVEL = 'info'
    APP_SERVICE_VERSION = 'v1.0.0'
