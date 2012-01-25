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