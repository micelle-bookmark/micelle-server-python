# coding=utf-8
'''API接口帮助模块'''

from functools import wraps

from flask import jsonify, request

from .AppError import ApiArgsError, AppErrorBase
from .LogHelper import CLogHelper
from .utils import format_exception, make_correct_resp, make_error_resp

# 日志输出对象
_log = CLogHelper.logger

# TODO: 尝试使用元类来序列化参数

def is_argument_exists(req_args, args_name):
    """
    判断参数是否存在.

    args:
        req_args: 请求参数字典
        args_name: 必需的参数名称列表

    return:
        None. 所有参数都存在
        string. 不存在的参数名
    """
    for arg_name in args_name:
        if arg_name not in req_args:
            return arg_name
    return None


def parse_post_args(req):
    """
    解析post请求的json参数体, 约定POST请求的参数使用http body传递.

    args:
        req: flask.request实体

    return:
        解析得到的参数字典. 可为None.

    exception:
        ApiArgsError.
    """
    if not req.is_json:
        raise ApiArgsError(1, u'需要json格式的请求体')

    try:
        req_args = req.get_json()
        return req_args
    except:
        raise ApiArgsError(5, u'参数json反序列化错误')


def post_check_args(req, args_name):
    '''
    校验POST请求中的参数. args_name长度为0时不解析参数, 返回None.

    args:
        req: flask.request实体
        args_name: 参数名称列表，例如['name', 'password']

    return:
        解析得到的参数字典. 可为None.

    exception:
        ApiArgsError.
    '''
    if len(args_name) == 0:
        return None

    req_args = parse_post_args(req)

    non_exists_name = is_argument_exists(req_args, args_name)
    if non_exists_name:
        raise ApiArgsError(2, u'缺少参数 {}'.format(non_exists_name))
    return req_args


def get_check_args(req, args_name):
    '''
    校验GET请求中的参数. args_name长度为0时不解析参数, 返回None. 约定GET请求的参数在url中传递

    args:
        req: flask.request实体
        args_name: 参数名称列表，例如['name', 'password']

    return:
        解析得到的参数字典. 可为None.

    exception:
        ApiArgsError.
    '''
    if len(args_name) == 0:
        return None

    req_args = req.values
    non_exists_name = is_argument_exists(req_args, args_name)
    if non_exists_name:
        raise ApiArgsError(2, u'缺少参数 {}'.format(non_exists_name))
    return req_args


class ArgsType(object):
    '''参数单元定义'''
    def __init__(self, name, convert=None, dest_name=None, require=True):
        '''
        args:
            name: 参数名
            convert: 转换为目标类型
            dest_name: 目标名称
            require: 是否必须
        '''
        self.name = name
        self.convert = convert
        self.dest_name = dest_name
        self.require = require


class ArgsChecker(object):
    '''参数检查类'''

    def __init__(self, names):
        '''
        args:
            names: 参数名列表
        '''
        assert isinstance(names, (list,))

        self.names = names
        super(ArgsChecker, self).__init__()

    def __call__(self, curr_req):
        raise NotImplementedError


class BodyArgsChecker(ArgsChecker):
    '''http body请求参数检查类'''

    def __init__(self, names):
        '''
        args:
            names: 参数名列表
        '''
        super(BodyArgsChecker, self).__init__(names)

    def __call__(self, curr_req):
        raise NotImplementedError


class UrlArgsChecker(ArgsChecker):
    '''http url请求参数检查类'''

    def __init__(self, names):
        '''
        args:
            names: 参数名列表
        '''
        super(UrlArgsChecker, self).__init__(names)

    def __call__(self, curr_req):
        raise NotImplementedError


class AuthChecker(ArgsChecker):
    '''登录认证检查类'''
    def __init__(self):
        super(AuthChecker, self).__init__([])

    def __call__(self, curr_req):
        raise NotImplementedError


def api_require_check(checker):
    '''
    API接口请求参数校验装饰器

    args:
        checker: 参数检查类
    '''
    def _api_require_check_wrapper(fn):
        '''
        请求校验包装函数, 校验通过则调用fn, 否则抛出AppErrorBase异常

        args:
            fn: 请求处理函数
        '''
        @wraps(fn)
        def __wrapper(**kwargs):
            try:
                args = checker(request)
                kwargs.update(args)
                r = fn(**kwargs)
                return jsonify(make_correct_resp(r))
            except AppErrorBase as ex:
                _log.error(unicode(ex))
                return jsonify(make_error_resp(ex.error_code, ex.error_msg))
            except Exception as ex:
                _log.critical(u'[未知错误]{}'.format(format_exception(ex)))
                return jsonify(make_error_resp(999, u'未知错误'))
        return __wrapper
    return _api_require_check_wrapper


def post_require_check(args_name):
    '''
    decorator.
    用于校验POST请求中的参数是否存在. 参数在http body中, json字符串.
    '''

    def post_require_check_wrapper(fn):
        '''
        包装函数.
        校验POST请求中的参数, 通过则用调用fn. 否则抛出AppErrorBase异常.
        '''

        @wraps(fn)
        def __wrapper(**arg):
            try:
                args = None
                if len(args_name):
                    args = post_check_args(request, args_name)
                r = fn(args, **arg)
                return jsonify(make_correct_resp(r))
            except AppErrorBase as ex:
                _log.error(unicode(ex))
                return jsonify(make_error_resp(ex.error_code, ex.error_msg))
            except Exception as ex:
                _log.critical(u'[未知错误]{}'.format(format_exception(ex)))
                return jsonify(make_error_resp(999, u'未知错误'))

        return __wrapper

    return post_require_check_wrapper


def get_require_check(args_name):
    '''
    decorator.
    用于校验GET请求中的参数是否存在. 参数在http url中.
    '''

    def get_require_check_wrapper(fn):
        '''
        包装函数.
        校验GET请求中的参数, 通过则用调用fn. 否则抛出AppErrorBase异常.
        '''

        @wraps(fn)
        def __wrapper(**arg):
            try:
                args = None
                if len(args_name):
                    args = get_check_args(request, args_name)
                r = fn(args, **arg)
                return jsonify(make_correct_resp(r))
            except AppErrorBase as ex:
                _log.error(unicode(ex))
                return jsonify(make_error_resp(ex.error_code, ex.error_msg))
            except Exception as ex:
                _log.critical(u'[未知错误]{}'.format(format_exception(ex)))
                return jsonify(make_error_resp(999, u'未知错误'))

        return __wrapper

    return get_require_check_wrapper
