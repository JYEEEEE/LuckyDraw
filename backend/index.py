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


class RegisterHandler(RequestHandler):
    """
    用户注册
        1.input：{'_id':ObjectID,       ID：自动生成
                  'login_name':str,     注册名：手机号/邮箱
                  'login_pass':str,     密码
                  'nick_name':str,      昵称
                  'balance':float,      账户余额：默认为0
                  'created_dt:str'}     创建时间
        2.output: 1   -> 注册成功
                  2   -> login_name重复
                  3   -> nick_name重复
                  4   -> 填写信息不全
                  -1  -> 服务器异常
    """

    def get(self):
        self.render('../templates/register.html')

    def post(self):
        ret_dict = {'code': 0}
        login_name = self.get_argument('login_name', '')
        login_pass = self.get_argument('login_pass', '')
        nick_name = self.get_argument('nick_name', '')

        if not login_name or login_pass or nick_name:
            ret_dict = {'code': 4}
            self.write(json.dumps(ret_dict))
            return

        login_name_result, nick_name_result, _ = user_info_search(login_name=login_name, nick_name=nick_name)
        if login_name_result:
            ret_dict['code'] = 2
            self.write(json.dumps(ret_dict))
            return

        if nick_name_result:
            ret_dict['code'] = 3
            self.write(json.dumps(ret_dict))
            return

        new_user = users_info.insert_one(
            {'login_name': login_name, 'login_pass': login_pass, 'nick_name': nick_name, 'balance': 0.0,
             'created_dt': time.time()})
        if new_user.inserted_id:
            ret_dict['code'] = 1
            self.write(json.dumps(ret_dict))
            return

        else:
            ret_dict['code'] = -1
            self.write(json.dumps(ret_dict))
            return


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
