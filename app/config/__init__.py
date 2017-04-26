# coding=utf-8
'''配置初始化'''

import os


def load_config():
    '''
    根据环境变量的值读取配置
    '''
    try:
        mode = os.environ.get("APP_MODE")

        if mode == 'PRODUCTION':
            from .production import ProductionConfig
            return ProductionConfig
        elif mode == 'TESTING':
            from .testing import TestingConfig
            return TestingConfig
        else:
            from .development import DevelopmentConfig
            return DevelopmentConfig
    except ImportError:
        from .default import Config
        return Config
