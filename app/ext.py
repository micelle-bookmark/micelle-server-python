# coding=utf-8
'''扩展模块'''

from flask_redis import FlaskRedis
from flask_sqlalchemy import SQLAlchemy

from core.ConfigHelper import CConfigHelper
from core.LogHelper import CLogHelper

# log对象
log = CLogHelper()

# config对象
conf = CConfigHelper()

# db对象
db = SQLAlchemy()

# cache对象
cache = FlaskRedis()
