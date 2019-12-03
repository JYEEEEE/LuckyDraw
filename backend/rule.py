#! /usr/bin/python

"""
@author: jyeeee
@contact: 807806181@qq.com
@time: 2019/12/2 15:57
"""
from bson import ObjectId
from tornado.web import RequestHandler

from backend.decorators import render_template, render_json
from database.models import Rule


class RuleListHandler(RequestHandler):
    """
    抽奖规则列表
    """

    @render_template('rule/list.html')
    def get(self):
        rules = Rule.find({})
        return locals()


class RuleAddHandler(RequestHandler):
    """
    新增规则
    """

    @render_template('rule/add.html')
    def get(self):
        return locals()

    @render_json
    def post(self):
        ret_dict = {'code': 0}

        name = self.get_argument('name')
        if not name:
            ret_dict['code'] = 2
            return ret_dict

        rule = Rule.find_one({'name': name})
        if rule:
            ret_dict['code'] = 3
            return ret_dict

        rule = Rule()
        rule.name = name
        comment = self.get_argument('comment')
        if comment:
            rule.comment = comment

        rule.save()
        ret_dict['code'] = 1
        return ret_dict


class RuleEditHandler(RequestHandler):
    """
    编辑规则
    """

    @render_template('rule/edit.html')
    def get(self):
        _id = self.get_argument('id')
        if not _id:
            raise ValueError('no _id')

        rule = Rule.find_one({'_id': ObjectId(_id)})
        if not rule:
            raise ValueError('no rule')

        return locals()

    @render_json
    def post(self):
        ret_dict = {'code': 0}

        name = self.get_argument('name')
        if not name:
            ret_dict['code'] = 2
            return ret_dict

        rule = Rule.find_one({'name': name})
        if not rule:
            ret_dict['code'] = 3
            return ret_dict

        rule.name = name
        comment = self.get_argument('comment')
        if comment:
            rule.comment = comment

        rule.save()
        ret_dict['code'] = 1
        return ret_dict
