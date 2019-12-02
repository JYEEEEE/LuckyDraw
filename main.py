import os

import tornado.ioloop
import tornado.web

from backend.auth import LoginHandler, RegisterHandler
from backend.index import MainHandler
from backend.rule import RuleListHandler, RuleAddHandler


def make_app():
    setting = dict(
        template_path=os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates"),
        static_path=os.path.join(os.path.dirname(os.path.abspath(__file__)), "static"),
    )

    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/register", RegisterHandler),
        (r"/login", LoginHandler),
        (r"/rule/list", RuleListHandler),
        (r"/rule/add", RuleAddHandler),
    ], **setting)


if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
