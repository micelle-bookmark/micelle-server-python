# coding=utf-8
'''
用户接口
'''

from flask.blueprints import Blueprint

from base import ApiHelper, AppError, ErrorCode
from ext import log

# 蓝图对象
bp = Blueprint('user', __name__)
# 蓝图url前缀
url_prefix = '/user/'


def _gen_token(key, expires, user_id):
    from itsdangerous import TimedJSONWebSignatureSerializer
    token = TimedJSONWebSignatureSerializer(secret_key=key, expires_in=expires)
    return token.dumps({'id': user_id})


class UserRegisterArgs(object):
    """用户注册接口参数"""

    @staticmethod
    def load(args):
        if 'email' not in args or \
           'password' not in args:
            raise AppError.ApiArgsError(
                ErrorCode.ERROR_API_ARGS_VALIDATION_FAIL,
                u"缺少参数 password 或者 email"
            )

        r = UserRegisterArgs()
        r.password = args['password']
        r.email = args['email']
        return r

    def __unicode__(self):
        return u'[{}] email={}, password={}'.format(
            self.__class__.__name__,
            self.email,
            self.password
        )


@bp.route("register", methods=["POST"])
@ApiHelper.api_post_args_parser(UserRegisterArgs)
def api_user_register(register_args):
    """
    用户注册接口
    """
    return {}


class UserLoginArgs(object):
    """用户登录接口参数"""

    @staticmethod
    def load(args):
        if 'email' not in args or \
           'password' not in args:
            raise AppError.ApiArgsError(
                ErrorCode.ERROR_API_ARGS_VALIDATION_FAIL,
                u"缺少参数 password 或者 email"
            )

        r = UserLoginArgs()
        r.password = args['password']
        r.email = args['email']
        return r

    def __unicode__(self):
        return u'[{}] email={}, password={}'.format(
            self.__class__.__name__,
            self.email,
            self.password
        )


@bp.route("login", methods=["POST"])
@ApiHelper.api_post_args_parser(UserLoginArgs)
def api_user_login(login_args):
    """用户登录接口"""
    return {}
