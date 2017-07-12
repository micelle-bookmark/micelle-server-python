# coding=utf-8
'''扩展模块'''

from flask_redis import FlaskRedis
from flask_sqlalchemy import SQLAlchemy

from base.ConfigHelper import CConfigHelper
from base.LogHelper import CLogHelper

# log对象
log = CLogHelper()

# config对象
conf = CConfigHelper()

# db对象
db = SQLAlchemy()

# cache对象
cache = FlaskRedis()
