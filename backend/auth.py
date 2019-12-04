#! /usr/bin/python

"""
@author: jyeeee
@contact: 807806181@qq.com
@time: 2019/12/2 14:25
"""
import traceback

from tornado.web import RequestHandler

from backend.decorators import render_json, render_template
from caches.redis_utils import RedisCache
from database.models import User
from utils import md5


class LoginHandler(RequestHandler):
    """
    用户登录：
        1.input:{'login_name':str,'login_pass':str}
        2.output:1   ->登陆成功
                 2   ->没有该用户
                 3   ->密码错误
                 4   ->参数错误
                 -1  ->服务器异常
    """

    @render_template("login.html")
    def get(self):
        return {}

    @render_json
    def post(self):
        ret_dict = {'code': 0}
        login_name = self.get_argument('login_name', '')
        login_pass = self.get_argument('login_pass', '')

        print(type(login_name), login_name, md5(login_name))

        if not login_name or not login_pass:
            ret_dict['code'] = 4
            return ret_dict

        try:
            user = User.find_one({'login_name': login_name})

            if not user:
                ret_dict['code'] = 2
                return ret_dict

            # tips: 密码通常不会明文保存在数据库中
            if md5(login_pass) == user.login_pass:
                ret_dict['code'] = 1
            else:
                key = 'login_fail_limit' + str(user._id)
                count = RedisCache.get(key)
                if count:
                    if isinstance(count, bytes):
                        count = count.decode('utf-8')
                    if isinstance(count, str):
                        count = int(count)
                else:
                    count = 0

                # 设置
                count += 1
                RedisCache.set(key, count, 5 * 60)
                if count >= 3:
                    ret_dict['code'] = -4
                else:
                    ret_dict['code'] = -3
        except Exception:
            print(traceback.format_exc())  # 打印出错时的异常栈信息
            ret_dict['code'] = -1

        return ret_dict


class RegisterHandler(RequestHandler):
    """
    用户注册
    """

    @render_template("register.html")
    def get(self):
        return {}

    @render_json
    def post(self):
        ret_dict = {'code': 0}
        login_name = self.get_argument('login_name', '')
        login_pass = self.get_argument('login_pass', '')

        if not login_name or not login_pass:
            ret_dict = {'code': 4}
            return ret_dict

        user = User.find_one(dict(login_name=login_name))
        if not user:
            user = User()
            user.login_name = login_name
            user.login_pass = md5(login_pass)
            user.save()
            ret_dict['code'] = 1
        else:
            ret_dict['code'] = 2
        return ret_dict
