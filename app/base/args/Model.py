# coding=utf-8

'''参数模型基类'''

from .ModelMetaclass import ModelMetaclass


class Model(object):
    '''参数模型基类'''

    __metaclass__ = ModelMetaclass


    def __init__(self):
        super(Model, self).__init__()
