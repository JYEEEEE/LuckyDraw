#! /usr/bin/python

"""
@author: yan.zhao
@contact: yan.zhao@idiaoyan.com
@time: 2019/10/14 16:55
"""
from pymongo import MongoClient

client = MongoClient('192.168.10.21', 27017)
db = client.LuckyDraw


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

    @classmethod
    def get_collection(cls):
        """
        获取表
        :return:
        """
        return db[cls.__name__.upper()]

    @classmethod
    def find_one(cls, query):
        return cls.get_collection().find_one(query)

    @classmethod
    def find(cls, query):
        return cls.get_collection().find(query)

    def save(self):
        mongo_dict = self.to_mongo()
        return self.get_collection().insert_one(mongo_dict)


class User(BaseModel):
    """
    用户表
    """
    login_name: str = None
    login_pass: str = None
