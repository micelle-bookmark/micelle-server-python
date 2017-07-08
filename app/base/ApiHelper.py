# coding=utf-8
'''API接口帮助模块'''

from functools import partial, wraps

from flask import jsonify, request

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


def api_args_parser(cls, loads_fn, name="cls"):
    """
    参数解析装饰器

    cls:
        参数类, 需要实现 load 接口
    """
    def _api_parser_wrapper(fn):
        """
        args:
            fn: 处理函数
        """
        @wraps(fn)
        def __wrapper(*klargs, **kwargs):
            try:
                args = cls.load(loads_fn(request))
                kwargs[name] = args
                r = fn(*klargs, **kwargs)
                if not isinstance(r, ('dict')):
                    r = r.dump()
                return jsonify(make_correct_resp(r))
            except AppErrorBase as ex:
                _log.error(unicode(ex))
                return jsonify(make_error_resp(ex.error_code, ex.error_msg))
            except Exception as ex:
                _log.critical(u'[未知错误]{}'.format(format_exception(ex)))
                return jsonify(make_error_resp(999, u'未知错误'))
        return __wrapper
    return _api_parser_wrapper


api_get_args_parser = partial(api_args_parser, loads_fn=_loads_get_args)
api_post_args_parser = partial(api_args_parser, loads_fn=_loads_post_args)
