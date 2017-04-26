# coding=utf-8
''' 配置模块 '''

class CConfigHelper(object):
    ''' 配置类 '''

    def __init__(self):
        ''' 配置类初始化 '''
        self.config_obj = None
        super(CConfigHelper, self).__init__()


    def init_app(self, app):
        '''
        配置类初始化

        args:
            app: flask app对象
        '''
        self.config = app.config

    @property
    def config(self):
        '''获取当前应用配置'''
        return self.config_obj

    @config.setter
    def config(self, obj):
        '''
        设置当前应用配置

        args:
            obj: 配置字典, dict
        '''
        self.config_obj = obj
