# coding:utf-8
''' Front end for Qzone Liker bot to activate program

author: build2last
'''

import os
import random
import time
import multiprocessing
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from tornado.options import define, options
import biz.Qliker as Qliker
import conf

define("port", default=conf.PORT, help="run on the given port", type=int)

# 初始化删除残留的QRCode文件
if os.path.exists(conf.QRCode_PATH):
    os.remove(conf.QRCode_PATH)

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        global USER_LIST, QRCODE_CRUD_LOCK
        # 存在二维码文件则不新创建子进程
        if not os.path.isfile(conf.QRCode_PATH):
            t = multiprocessing.Process(target=Qliker.exe, args=(QRCODE_CRUD_LOCK, USER_LIST))
            t.start()
        self.render('index.html', uidlist=USER_LIST)

class LogHandler(tornado.web.RequestHandler):
    def get(self,input):
        if os.path.exists("log.log"):
            with open("log.log", "r") as fr:
                self.write("".join(fr.readlines()[-15:]))
        else:
            self.write("No log yet!")

if __name__ == '__main__':
    QRCODE_CRUD_LOCK = multiprocessing.Lock()
    MGR = multiprocessing.Manager()
    USER_LIST = MGR.list()
    tornado.options.parse_command_line()
    app = tornado.web.Application(
        handlers=[(r'/', IndexHandler),
            (r'/api/v1/qrcode/(.*?)', tornado.web.StaticFileHandler, dict(path=conf.IMAGE_DIR)),
        ],
        template_path=os.path.join(os.path.dirname(__file__), "templates"),
        static_path=os.path.join(os.path.dirname(__file__), "static"),
        debug=True
    )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
