#! /usr/bin/python

"""
@author: yan.zhao
@contact: yan.zhao@idiaoyan.com
@time: 2019/10/14 16:55
"""
from bson import ObjectId
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
            if k == '_id':
                if not v:
                    # 如果没有给定_id,那么由数据库自动生成
                    continue
                mongo_dict[k] = v
        return mongo_dict

    @classmethod
    def get_fields(cls):
        return filter(lambda x: not x.startswith('_') or x == '_id', cls.__dict__)

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
        if '_id' in mongo_dict:
            _id = mongo_dict.pop('_id')
            if not isinstance(_id, ObjectId):
                _id = ObjectId(_id)
            return self.get_collection().update_one({'_id': _id}, mongo_dict, upsert=True)
        else:
            return self.get_collection().insert_one(mongo_dict)


class User(BaseModel):
    """
    用户表
    """
    _id: ObjectId = None
    login_name: str = None
    login_pass: str = None


class Rule(BaseModel):
    _id: ObjectId = None
    name: str = ""
    comment: str = ""
