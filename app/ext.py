# coding=utf-8
'''扩展模块'''

from flask_redis import FlaskRedis

from base.ConfigHelper import CConfigHelper
from base.LogHelper import CLogHelper

# from flask_sqlalchemy import SQLAlchemy


# log对象
log = CLogHelper()

# config对象
conf = CConfigHelper()

# db对象
# db = SQLAlchemy()

# cache对象
cache = FlaskRedis()
