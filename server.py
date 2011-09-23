#!/usr/bin/env python

import tornado.ioloop
import tornado.web

import handlers

application = tornado.web.Application([
    (r'/', handlers.IndexHandler)
])

if __name__ == '__main__':
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()