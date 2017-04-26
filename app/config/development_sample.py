# coding=utf-8
'''开发配置模板'''

from .default import Config


class DevelopmentConfig(Config):
    '''
    开发环境配置数据
    '''

    # Flask config
    DEBUG = True
