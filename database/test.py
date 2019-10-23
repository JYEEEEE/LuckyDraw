#! /usr/bin/python

"""
@author: yan.zhao
@contact: yan.zhao@idiaoyan.com
@time: 2019/10/15 15:16
"""
from database.models import User


def test_to_mongo():
    user = User()
    user.login_name = 'test'
    user.login_pass = 'test'

    print(user.to_mongo())


def test_find_one():
    ret = User.find_one({'login_name': 'test3'})
    print(ret)
    print(ret.login_name)


def test_find():
    u_list = User.find({'login_name': None})
    print(u_list)
    for u in u_list:
        print('user:', u)
        print('user.login_name: ', u.login_name)
        print('user.to_mongo:', u.to_mongo())


def test_save():
    user = User()
    user.login_name = 'test3'
    user.login_pass = 'test3'
    print(user.save())


test_find()
# test_save()
