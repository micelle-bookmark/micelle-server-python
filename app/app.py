# coding=utf-8
'''Flask app'''

from flask import Flask
from werkzeug.utils import find_modules, import_string


def register_blueprints(root, var_app):
    '''
    蓝图注册帮助函数

    args:
        root: 蓝图所在模块
        app: Flask实例
    '''
    for name in find_modules(root, recursive=False):
        mod = import_string(name)
        if hasattr(mod, 'bp') and hasattr(mod, 'url_prefix'):
            var_app.register_blueprint(mod.bp, url_prefix=mod.url_prefix)


def create_app():
    '''
    创建flask app对象
    '''
    app_obj = Flask(__name__)

    from config import load_config
    app_obj.config.from_object(load_config())

    from ext import log, conf, db, cache
    log.init_app(app_obj)
    conf.init_app(app_obj)
    db.init_app(app_obj)
    cache.init_app(app_obj)

    register_blueprints('views', app_obj)

    return app_obj


# 应用app对象
app = create_app()

if __name__ == '__main__':
    app.run()
