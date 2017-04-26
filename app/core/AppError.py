# coding=utf-8
""" 应用异常定义 """


class AppErrorBase(Exception):
    """
    应用错误基类
    """

    def __init__(self, code, msg):
        """
        args:
            code: 错误码
            msg: 错误信息
        """
        self.error_code = code
        self.error_msg = msg
        super(AppErrorBase, self).__init__()

    def __unicode__(self):
        """
        返回打印字符串
        """
        return u'[错误码{}], {}'.format(self.error_code, self.error_msg)


class ApiArgsError(AppErrorBase):
    """
    接口参数错误类
    """

    def __unicode__(self):
        """
        返回打印字符串
        """
        return u'[参数错误]{}'.format(super(ApiArgsError, self).__unicode__())


class DatabaseError(AppErrorBase):
    """
    数据库操作错误类
    """

    def __unicode__(self):
        """
        返回打印字符串
        """
        return u'[数据库错误]{}'.format(super(DatabaseError, self).__unicode__())


class AppError(AppErrorBase):
    """
    应用逻辑错误
    """

    def __unicode__(self):
        """
        返回打印字符串
        """
        return u'[应用错误]{}'.format(super(AppError, self).__unicode__())
