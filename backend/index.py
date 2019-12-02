import json
import time

from tornado.web import RequestHandler

from database.users_info import user_info_search


class MainHandler(RequestHandler):
    """
    欢迎页渲染
    """

    def get(self):
        self.redirect("/login")


class HomeHandler(RequestHandler):
    """
    主页渲染
    """

    def get(self):
        self.write("待定，选择用户操作")

    def post(self):
        pass



class LoginHandler(RequestHandler):
    """
    用户登录：
        1.input:{'login_name':str,'login_pass':str}
        2.output:1   ->登陆成功
                 2   ->没有该用户
                 3   ->密码错误
                 -1  ->服务器异常
    """

    def get(self):
        self.render('../templates/login.html')

    def post(self):
        ret_dict = {'code': 0}
        login_name = self.get_argument('login_name', '')
        login_pass = self.get_argument('login_pass', '')
        login_name_result, login_pass_result, _ = user_info_search(login_name=login_name, login_pass=login_pass)

        if not login_name_result:
            ret_dict['code'] = 2

        if login_name_result:
            if login_pass_result:
                ret_dict['code'] = 1
            else:
                ret_dict['code'] = 3
        else:
            ret_dict['code'] = -1

        self.write(json.dumps(ret_dict))
        return
