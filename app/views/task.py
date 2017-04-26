# coding=utf-8
''' 定时任务接口 '''

from flask.blueprints import Blueprint

from core import AppError, utils
from ext import log


# 蓝图对象
bp = Blueprint('task', __name__)
# 蓝图url前缀
url_prefix = '/task'


@bp.route('', methods=['GET'])
@utils.get_require_check(['type'])
def api_task_index(args):
    '''
    定时任务接口

    args:
        args.type: 未使用
    '''
    return {}

