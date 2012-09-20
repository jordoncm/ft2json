#!/usr/bin/env python
#
# Copyright 2012 Jordon Mears (http://www.finefrog.com/)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import tornado.ioloop
import tornado.web

import handlers

application = tornado.web.Application([
    (r'/', handlers.IndexHandler),
    (r'/q/?', handlers.QueryHandler),
    (r'/query/?', handlers.QueryHandler),
    (r'/query-browser.html', handlers.QueryBrowserHandler),
    (r'/api/(.*)', tornado.web.StaticFileHandler, {'path' : './api'}),
    (r'/static/(.*)', tornado.web.StaticFileHandler, {'path' : './static'}),
    (r'/(crossdomain\.xml)', tornado.web.StaticFileHandler, {'path' : './'})
])

if __name__ == '__main__':
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()