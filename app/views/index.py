# coding=utf-8
'''服务信息'''

from flask import jsonify, request
from flask.blueprints import Blueprint

from ext import log

# 蓝图对象
bp = Blueprint('index', __name__)
# 蓝图url前缀
url_prefix = ''


@bp.route("/", methods=["GET"])
def api_index():
    """
    首页接口
    """
    log.info("index")

    return jsonify({"service": "micelle"})


# 这个 before 会对所有 request 生效
@bp.before_app_request
def _before_apop_request():
    log.info(u"Start Process URL: {}".format(request.url))
