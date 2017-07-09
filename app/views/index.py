# coding=utf-8
'''服务信息'''

import uuid

from flask import request
from flask.blueprints import Blueprint

from base import ApiHelper
from ext import log

# 蓝图对象
bp = Blueprint('index', __name__)
# 蓝图url前缀
url_prefix = ''


@bp.route("/", methods=["GET"])
@ApiHelper.api_get_args_parser(None)
def api_index():
    """
    首页接口
    """
    return {
        "service": "micelle",
        "version": "v1.0.0"
    }


# 这个 before 会对所有 request 生效
@bp.before_app_request
def _before_apop_request():
    log.sequence_id = uuid.uuid1().get_hex()
    log.info(u"{} {}".format(request.method, request.url))
