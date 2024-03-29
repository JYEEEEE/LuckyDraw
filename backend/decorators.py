#! /usr/bin/python

"""
@author: yan.zhao
@contact: yan.zhao@idiaoyan.com
@time: 2019/10/14 17:09
"""
import json


def render_json(func):
    """
    仅用于装饰post请求
    :param func:
    :return:
    """

    def wrapper(self, *args, **kwargs):
        data = func(self, *args, **kwargs)
        if not isinstance(data, dict):
            return data
        if 'self' in data.keys():
            del data['self']
        self.write(json.dumps(data))

    return wrapper


def render_template(template_path):
    """

    :param template_path:
    :return:
    """

    def deco(func):
        def wrapper(self, *args, **kwargs):
            data = func(self, *args, **kwargs)
            if not isinstance(data, dict):
                return data
            if 'self' in data.keys():
                del data['self']
            self.render(template_path, **data)

        return wrapper

    return deco
