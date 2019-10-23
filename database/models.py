#! /usr/bin/python

"""
@author: yan.zhao
@contact: yan.zhao@idiaoyan.com
@time: 2019/10/14 16:55
"""


class BaseModel(object):
    """
    数据库映射
    """

    def to_mongo(self):
        mongo_dict = {}
        for k, v in self.__dict__.items():
            if not k.startswith('_'):
                mongo_dict[k] = v
        return mongo_dict


class User(BaseModel):
    """
    用户表
    """
    login_name: str = None
    login_pass: str = None


user = User()
user.login_name = 'test'
user.login_pass = 'test'

print(user.to_mongo())
