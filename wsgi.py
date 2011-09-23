#!/usr/bin/env python

import tornado.web
import tornado.wsgi
import wsgiref.handlers

import handlers

application = tornado.wsgi.WSGIApplication([
    (r'/', handlers.IndexHandler)
])

def main():
    wsgiref.handlers.CGIHandler().run(application)

if __name__ == '__main__':
    main()