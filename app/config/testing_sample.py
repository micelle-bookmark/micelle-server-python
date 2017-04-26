# coding=utf-8
'''测试配置模板'''

from .default import Config


class TestingConfig(Config):
    '''
    测试环境配置数据
    '''

    # Flask config
    DEBUG = True
    TESTING = True
