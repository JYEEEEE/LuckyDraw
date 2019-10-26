#! /usr/bin/python

"""
@author: yan.zhao
@contact: yan.zhao@idiaoyan.com
@time: 2019/10/14 17:09
"""
import json


def render_json(func):
    def wrapper(self, *args, **kwargs):
        data = func(self, *args, **kwargs)
        if not isinstance(data, dict):
            return data
        if 'self' in data.keys():
            del data['self']
        self.write(json.dumps(data))

    return wrapper
