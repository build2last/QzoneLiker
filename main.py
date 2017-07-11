# coding:utf-8
# REST practice for Qzone Liker bot to activate program

import os
import random
import time
import threading

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from tornado.options import define, options
import QLiker
import conf

define("port", default=8080, help="run on the given port", type=int)

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        if not os.path.isfile(conf.QRCode_PATH):
            t = threading.Thread(target=QLiker.exe, args=())
            t.setDaemon(True)
            t.start()
        wait_count = 0
        # while not os.path.isfile(conf.QRCode_PATH) and wait_count<3:
        #     wait_count += 1
        #     time.sleep(0.2)
        # self.set_header("Cache-Control", "no-cache")
        self.render('index.html')

class LogHandler(tornado.web.RequestHandler):
    def get(self,input):
        if os.path.exists("log.log"):
            with open("log.log", "r") as fr:
                self.write("".join(fr.readlines()[-15:]))
        else:
            self.write("No log yet!")

if __name__ == '__main__':
    tornado.options.parse_command_line()
    app = tornado.web.Application(
        handlers=[(r'/', IndexHandler),
            (r'/api/v1/qrcode/(.*?)', tornado.web.StaticFileHandler, dict(path=conf.IMAGE_DIR)),
        ],
        template_path=os.path.join(os.path.dirname(__file__), "templates"),
        static_path=os.path.join(os.path.dirname(__file__), "static"),
        debug=False
    )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()