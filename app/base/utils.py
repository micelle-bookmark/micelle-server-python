# coding=utf-8
''' tools '''

import traceback

from .AppError import ApiArgsError
from .LogHelper import CLogHelper

# 日志输出对象
_log = CLogHelper.logger


def make_error_resp(error_code, error_msg):
    """
    构造错误返回值

    args:
        error_code: 错误码
        error_msg: 错误信息

    return:
        字典.
    """
    return make_resp({}, error_code, error_msg)


def make_correct_resp(data=None):
    """
    构造正确返回值

    args:
        data: 返回数据

    return:
        字典.
    """
    if data is None:
        data = {}
    return make_resp(data, 0, 'success')


def make_resp(data, status, msg):
    """
    构造返回值

    args:
        data: 返回数据
        status: 错误码
        msg: 错误信息

    return:
        字典.
    """
    return {'data': data, 'errorCode': status, 'message': msg}


def format_exception(ex):
    """
    格式化异常的具体信息

    args:
        ex: 异常对象

    return:
        str.

    exception:
        不抛出异常.
    """
    return unicode(traceback.format_exc())


def format_resp_time(time_str):
    '''
    将数据库中时间字段格式化为返回所需
    YYYY-MM-DD HH:MM:SS -> MM-DD HH:MM

    args:
        time_str: 需格式化的时间, YYYY-MM-DD HH:MM:SS

    return:
        MM-DD HH:MM
    '''
    try:
        return str(time_str)[5:16]
    except Exception as ex:
        _log.critical(u'[未知错误]{}'.format(format_exception(ex)))
        return time_str


def parse_page_size_arg(args):
    """
    解析page和size参数.

    args:
        args.page: 页码
        args.size: 数量

    return:
        (page, size)

    exception:
        ApiArgsError.
    """
    page = parse_type_arg(args, 'page', int)
    if page < 1:
        raise ApiArgsError(110, u'参数 page={} 取值错误, 范围 >=1'.format(page))

    size = parse_type_arg(args, 'size', int)
    if size < 1:
        raise ApiArgsError(110, u'参数 size={} 取值错误, 范围 >=1'.format(size))

    return page, size


def parse_offset_size_arg(args):
    """
    解析page和size参数并转换为offset, size

    args:
        args.page: 页码
        args.size: 数量

    return:
        (offset, size)

    exception:
        ApiArgsError.
    """
    page, size = parse_page_size_arg(args)
    return (page - 1) * size, size


def parse_start_size_arg(args, size=10):
    """
    解析 start和size参数

    args:
        args.start: 起始偏移量
        args.size: 数量参数, 不存在时取默认值

    return:
        (start, size)

    exception:
        ApiArgsError.
    """
    start = parse_type_arg(args, 'start', int)
    if start < 0:
        raise ApiArgsError(110, u'参数 start={} 取值错误, 范围 >=0'.format(start))

    new_size = size
    if 'size' in args:
        new_size = parse_type_arg(args, 'size', int)
    if new_size < 1:
        raise ApiArgsError(110, u'参数 size={} 取值错误, 范围 >=1'.format(new_size))

    return start, size


def parse_status_arg(args, expect):
    """
    解析status 参数.

    args:
        args.status: 状态值
        expect: 预期范围

    return:
        status

    exception:
        ApiArgsErrorst.
    """
    status = parse_type_arg(args, 'status', int)
    if status not in expect:
        raise ApiArgsError(110, u'参数 status={} 取值错误, 预期值{}'.format(status,
                                                                   expect))
    return status


def parse_type_arg(args, key, t):
    """
    解析args中的key参数.

    args:
        args: 参数字典
        key: 参数名
        t: 参数类型

    return:
        t类型的值.

    exception:
        ApiArgsError.
    """
    try:
        v = t(args[key])
        return v
    except ValueError:
        raise ApiArgsError(116, u'参数{}不是{}.'.format(key, t))


def second():
    '''
    获取当前秒数
    '''
    import time
    return int(time.time())


# 一天的秒数
second_per_day = 60*60*24
