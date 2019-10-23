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
    print(User.find_one({'login_name': 'test'}))


def test_save():
    user = User()
    user.login_name = 'test'
    user.login_pass = 'test'
    print(user.save())


test_find_one()
# test_save()
