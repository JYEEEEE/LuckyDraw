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
    def get_fields(cls):
        return filter(lambda x: not x.startswith('_'), cls.__dict__)

    @classmethod
    def get_collection(cls):
        """
        获取表
        :return:
        """
        return db[cls.__name__.upper()]

    @classmethod
    def find_one(cls, query):
        result = cls.get_collection().find_one(query)
        if not result:
            return result

        clazz = cls()
        for k in cls.get_fields():
            setattr(clazz, k, result.get(k))
        return clazz

    @classmethod
    def find(cls, query):
        results = cls.get_collection().find(query)

        clazz_list = []
        for ret in results:
            clazz = cls()
            for k in cls.get_fields():
                setattr(clazz, k, ret.get(k))
            clazz_list.append(clazz)

        return clazz_list

    def save(self):
        mongo_dict = self.to_mongo()
        return self.get_collection().insert_one(mongo_dict)


class User(BaseModel):
    """
    用户表
    """
    login_name: str = None
    login_pass: str = None


class Rule(BaseModel):
    name: str = ""
    comment: str = ""
