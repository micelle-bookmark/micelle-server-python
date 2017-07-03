# coding=utf-8

'''参数模型'''


class ModelMetaclass(type):
    '''参数模型元类'''

    def __new__(mcs, name, bases, attrs):
        '''
        新建参数模型对象

        args:
            mcs: 当前实例
            name: 类名
            bases: 父类元组
            attrs: 属性字典
        '''
        if name == 'Model':
            return super(ModelMetaclass, mcs).__new__(mcs, name, bases, attrs)

        return super(ModelMetaclass, mcs).__new__(mcs, name, bases, attrs)
