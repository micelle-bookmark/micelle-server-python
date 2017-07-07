# coding=utf-8
'''API接口帮助模块'''

from functools import wraps

from flask import jsonify, request
from marshmallow import ValidationError

from core import ErrorCode
from core.AppError import ApiArgsError, AppErrorBase
from core.LogHelper import CLogHelper
from core.utils import format_exception, make_correct_resp, make_error_resp

# 日志输出对象
_log = CLogHelper.logger


def _loads_post_args(req):
    """
    解析 POST 请求的参数, 约定使用 HTTP BODY 传递, 格式为 json.

    args:
        req: flask.request实体

    return:
        解析得到的参数字典. 可为None.

    exception:
        ApiArgsError.
    """
    if not req.is_json:
        raise ApiArgsError(ErrorCode.ERROR_POST_ARGS_MUST_BE_JSON,
                           u"POST 请求参数需要 JSON 格式的 HTTP BODY")

    try:
        r = req.get_json()
        return r
    except Exception as ex:
        raise ApiArgsError(ErrorCode.ERROR_POST_ARGS_LOADS_FAIL,
                           u"POST 请求中参数 LOADS 错误, {}".format(unicode(ex)))


def _loads_get_args(req):
    """
    解析 GET 请求的参数, 约定使用 URL 传递.

    args:
        req: flask.request实体

    return:
        解析得到的参数字典. 可为None.

    exception:
        ApiArgsError.
    """
    return req.values





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
