# coding=utf-8

'''参数模型'''


class Model(type):
    '''参数模型元类'''

    def __new__(mcs, name, bases, dct):
        '''
        新建参数模型对象

        args:
            mcs: 当前实例
            name: 类名
            bases: 父类元组
            dct: 属性字典
        '''
        return super(Model, mcs).__new__(mcs, name, bases, dct)
