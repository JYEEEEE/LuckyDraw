import os
import tornado.ioloop
import tornado.web

def make_app():
    setting = dict(
        template_path=os.path.join(os.path.dirname(__file__), "templates"),
        static_path=os.path.join(os.path.dirname(__file__), "static"),
    )

    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/register", RegisterHandler),
        (r"/login", LoginHandler)
    ], **setting)


if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
