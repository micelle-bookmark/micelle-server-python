# coding=utf-8
'''
用户接口
'''

from flask.blueprints import Blueprint

from base import AppError, utils
from ext import log
from module.auth import AuthHelper

# 蓝图对象
bp = Blueprint('user', __name__)
# 蓝图url前缀
url_prefix = '/user/'


def _gen_token(key, expires, user_id):
    from itsdangerous import TimedJSONWebSignatureSerializer
    token = TimedJSONWebSignatureSerializer(secret_key=key, expires_in=expires)
    return token.dumps({'id': user_id})


@bp.route("register", methods=["GET"])
def api_user_register():
    """
    用户注册接口
    """
    log.info("user register")
    pass
