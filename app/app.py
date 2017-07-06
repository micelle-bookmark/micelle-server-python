# coding=utf-8
'''Flask app'''

import inspect

from flask import Flask
from werkzeug.utils import find_modules, import_string


def _register_blueprints(root, var_app):
    '''
    蓝图注册帮助函数

    args:
        root: 蓝图所在模块
        var_app: Flask实例
    '''
    for name in find_modules(root, recursive=False):
        mod = import_string(name)
        if hasattr(mod, 'bp') and hasattr(mod, 'url_prefix'):
            print 'loading module {}'.format(name)
            var_app.register_blueprint(mod.bp, url_prefix=mod.url_prefix)


def _init_ext_module(var_app):
    '''
    ext 模块初始化函数

    args:
        var_app: Flask实例
    '''
    def _is_variable(attr):
        return not inspect.isclass(attr) and not inspect.ismodule(attr)

    def _process_with_attr(attr_name, m):
        attr = getattr(m, attr_name)
        if _is_variable(attr):
            fn = getattr(attr, 'init_app', None)
            if callable(fn):
                print 'calling {}.{}'.format(attr_name, 'init_app')
                fn(var_app)

    import ext
    [_process_with_attr(attr_name, ext) for attr_name in dir(ext)]


def create_app():
    '''
    创建flask app对象
    '''
    app_obj = Flask(__name__)

    from config import load_config
    app_obj.config.from_object(load_config())

    _init_ext_module(app_obj)

    _register_blueprints('views', app_obj)

    return app_obj


# 应用app对象
app = create_app()

if __name__ == '__main__':
    # use_reloader disable App load twice
    app.run(use_reloader=False)
