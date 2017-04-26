# coding=utf-8
'''
用户接口
'''

from flask.blueprints import Blueprint

from core import AppError, utils
from ext import conf, log
from module.auth import AuthHelper
from module.user import UserHelper

# 蓝图对象
bp = Blueprint('user', __name__)
# 蓝图url前缀
url_prefix = '/api'


def _gen_token(key, expires, user_id):
    from itsdangerous import TimedJSONWebSignatureSerializer
    token = TimedJSONWebSignatureSerializer(secret_key=key, expires_in=expires)
    return token.dumps({'id': user_id})


@bp.route('/register', methods=['POST'])
@utils.post_require_check(['username', 'password', 'phoneNumber'])
def api_user_register(args):
    '''
    用户注册接口

    args: json
        username: 用户名
        password: 密码(密文)
        phoneNumber: 电话号码

    return:
        {'userId': ''}
    '''
    username = args['username']
    password = args['password']
    phone = args['phoneNumber']

    user = UserHelper.select_basic_from_phone(phone)
    if user:
        raise AppError.AppError(111, U'手机号={}已经注册'.format(phone))

    user = UserHelper.create(username, password, phone)
    log.info(
        u'注册用户成功, 用户名={}, 手机号={}, 用户id={}'.format(username, phone, user['id']))

    return {'userId': user['id']}


@bp.route('/user/login', methods=['POST'])
@utils.post_require_check(['phone', 'password'])
def api_user_login(args):
    '''
    用户登录接口

    args: json
        phone: 用户手机号
        password: 密码(密文)
        terminal:  终端类型，可选

    return:
        token: 用户token
        user.id: 用户id
        user.username: 用户名
        user.phone: 电话号码
        user.email: 邮箱
    '''
    phone = args['phone']
    password = args['password']

    if phone == '' or password == '':
        raise AppError.AppError(99, u'用户名或密码为空')

    user_obj = UserHelper.select_basic_from_phone(phone)
    if not user_obj:
        raise AppError.AppError(98, u'用户手机号未注册')

    if user_obj['password'] != password:
        raise AppError.AppError(97, u'密码错误')

    token = _gen_token(user_obj['id'], conf.config['SECRET_KEY'], 3600)
    AuthHelper.login(user_obj, token)

    log.info(u'用户id={}登录, token={}'.format(user_obj['id'], token))
    return {
        'token': token,
        'user': {
            'id': user_obj['id'],
            'username': user_obj['name'],
            'phone': user_obj['phone'],
            'email': user_obj['email']
        }
    }


@bp.route('/user/logout', methods=['POST'])
@utils.post_require_check([])
def api_user_logout(args):
    '''
    用户登出接口

    args:
        None.

    return:
        登出结果
    '''
    uid, token = AuthHelper.auth()
    log.info(u'用户id={}退出登录, token={}'.format(uid, token))
    AuthHelper.logout(token)
    return {}


@bp.route('/modifyUserInfo', methods=['POST'])
@utils.post_require_check([])
def api_user_modify_info(args):
    '''
    修改个人用户信息接口

    args:
        args: None

    return:
        修改结果
    '''
    from flask import request

    uid = AuthHelper.auth()[0]

    args = utils.parse_post_args(request)
    if len(args) == 0:
        log.info(u'调用修改个人信息接口但没有参数')
        return {}

    UserHelper.modify(uid, args)

    return {}


@bp.route('/getUserInfo', methods=['GET'])
@utils.get_require_check(['id'])
def api_user_get(args):
    '''
    获取用户个人信息接口

    args:
        args.id: 用户id

    return:
        user.userName: 用户名
        user.phoneNumber: 电话号码
        user.portrait: 头像url
        user.sex: 性别
        user.birthday: 出生日期
        user.emotionStatus: 情感状态
        user.personalProfile: 个人签名
        user.area: 地区
    '''
    user_id = args['id']
    user_info = UserHelper.get(user_id)
    if user_info:
        user_info['hasFocus'] = 0
        request_uid = AuthHelper.current_uid()
        if AuthHelper.INVALID_USER_ID != request_uid:
            # TODO 获取关注关系
            # user_info['hasFocus'] =
            pass
        return {'user': user_info}
    raise AppError.AppError(207, u'用户id={} 不存在'.format(user_id))


@bp.route('/user/statistic', methods=['GET'])
@utils.get_require_check(['id'])
def api_user_statistic(args):
    '''
    获取用户个人统计信息接口

    args:
        args.id: 用户id
    '''
    uid = utils.parse_type_arg(args, 'id', int)
    data = UserHelper.get_ex(uid)
    if data:
        return {'statistic': data}
    raise AppError.AppError(207, u'用户id={} 不存在'.format(uid))


@bp.route('/forgetPass', methods=['POST'])
@utils.post_require_check(['phoneNumber', 'passwd'])
def api_forget_password(args):
    '''
    忘记密码, 更新密码

    args:
        args.phoneNumber: 手机号
        args.passwd: 新密码
    '''
    phone = args['phoneNumber']
    user = UserHelper.select_basic_from_phone(phone)
    if not user:
        raise AppError.AppError(112, u'手机号{}未注册'.format(phone))

    new_passwd = args['passwd']
    update_opt = UserHelper.update_user_passwd(user["id"], new_passwd)
    return {}
