# coding=utf-8
'''登录认证模块'''

from flask import request

from base import AppError
from ext import cache

# 保存TOKEN值的redis.key
TOKEN_ID_KEY = 'hash:token.id'
# 无效的用户ID标识
INVALID_USER_ID = -1


def login(user, token):
    """
    当用户登录成功后调用此接口
     args:
        user: 用户数据, 字典
        token: 用户此次登录token
    """
    cache.hset(TOKEN_ID_KEY, token, user['id'])


def logout(token):
    '''
    当用户退出登录后调用此接口
     args:
        token: token字符串
    '''
    cache.hdel(TOKEN_ID_KEY, token)


def token_to_id(token):
    """
    根据用户token获取用户id

    args:
        token: token字符串

    return:
        int. UserId
    """
    user_id = cache.hget(TOKEN_ID_KEY, token)
    return int(user_id) if user_id else INVALID_USER_ID


def is_valid_token(token):
    """
    是否是有效的token
    args:
        token: token字符串
    return:
        bool
    """
    return INVALID_USER_ID != token_to_id(token)


def auth():
    '''
    验证用户是否登录

    args:
        无.

    return:
        (uid, token).

    exceptions:
        ApiArgsError
    '''
    if 'token' not in request.headers:
        raise AppError.ApiArgsError(3, u'需要token')

    token = request.headers.get('token')
    uid = token_to_id(token)
    if INVALID_USER_ID == uid:
        raise AppError.ApiArgsError(4, u'无效的token值 {}'.format(token))

    return uid, token


def current_uid():
    '''
    获取当前请求用户id

    args:
        无.

    return:
        uid. INVALID_USER_ID代表没有用户信息
    '''
    if 'token' not in request.headers:
        return INVALID_USER_ID

    token = request.headers.get('token')
    return token_to_id(token)
