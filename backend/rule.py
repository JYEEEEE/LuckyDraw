#! /usr/bin/python

"""
@author: jyeeee
@contact: 807806181@qq.com
@time: 2019/12/2 15:57
"""
from tornado.web import RequestHandler

from backend.decorators import render_template
from database.models import Rule


class RuleListHandler(RequestHandler):
    """
    抽奖规则列表
    """

    @render_template('rule/list.html')
    def get(self):
        rules = Rule.find({})
        return locals()
