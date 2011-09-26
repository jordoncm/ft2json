#!/usr/bin/env python

import tornado.web
import tornado.wsgi
import wsgiref.handlers

import handlers

application = tornado.wsgi.WSGIApplication([
    (r'/', handlers.IndexHandler),
    (r'/q/?', handlers.QueryHandler),
    (r'/query/?', handlers.QueryHandler),
    (r'/api/(.*)', tornado.web.StaticFileHandler, {'path' : './api'})
])

def main():
    wsgiref.handlers.CGIHandler().run(application)

if __name__ == '__main__':
    main()