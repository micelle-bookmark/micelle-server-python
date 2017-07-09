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
        if 'username' not in args or \
           'email' not in args:
            raise AppError.ApiArgsError(
                ErrorCode.ERROR_API_ARGS_VALIDATION_FAIL,
                u"缺少参数 username 或者 email"
            )

        r = UserRegisterArgs()
        r.username = args['username']
        r.email = args['email']
        return r

    def __unicode__(self):
        return u'[UserRegisterArgs] username={}, email={}'.format(
            self.username,
            self.email
        )


@bp.route("register", methods=["GET"])
@ApiHelper.api_get_args_parser(UserRegisterArgs)
def api_user_register(cls):
    """
    用户注册接口
    """
    log.info(u"user register, {}".format(unicode(cls)))
    return {}
