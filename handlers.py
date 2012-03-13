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

import csv
import httplib
try:
    import json
except ImportError:
    from django.utils import simplejson as json
import logging
import StringIO
import tornado.web
import tornado.template
import urllib

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        urlPrefix = ''
        if True:
            urlPrefix = self.request.protocol + '://' + self.request.host
        else:
            urlPrefix = self.request.protocol + '://' + self.request.host
        
        loader = tornado.template.Loader('templates')
        self.write(loader.load('index.html').generate(
            urlPrefix = urlPrefix
        ))
    
    def post(self):
        self.get()

class QueryBrowserHandler(tornado.web.RequestHandler):
    def get(self):
        loader = tornado.template.Loader('templates')
        self.write(loader.load('query.html').generate())
    
    def post(self):
        self.get()

class QueryHandler(tornado.web.RequestHandler):
    def get(self):
        getCommands = [
            'show',
            'describe',
            'select'
        ]
        
        postCommands = [
            'create',
            'insert',
            'update',
            'delete',
            'drop'
        ]
        
        output = {
            'data' : []
        }
        
        sql = self.get_argument('sql', '')
        
        if sql != '':
            try:
                type = sql.strip().split(' ')[0].lower()
                try:
                    if getCommands.index(type) >= 0:
                        method = 'get'
                except:
                    pass
                try:
                    if postCommands.index(type) >= 0:
                        method = 'post'
                except:
                    pass
                
                if type == 'select':
                    start = int(self.get_argument('start', 0))
                    limit = int(self.get_argument('limit', 100))
                    
                    sql += ' OFFSET ' + str(start) + ' LIMIT ' + str(limit)
                    
                    output['start'] = start
                    output['limit'] = limit
                
                parameters = {
                    'sql' : sql
                }
                accessToken = self.get_argument('access_token', '')
                if accessToken != '':
                    parameters['access_token'] = accessToken
                
                connection = httplib.HTTPSConnection(
                    'www.google.com',
                    timeout=120
                )
                if method == 'get':
                    connection.request(
                        'GET',
                        '/fusiontables/api/query?' + urllib.urlencode(parameters)
                    )
                elif method == 'post':
                    connection.request(
                        'POST',
                        '/fusiontables/api/query?' + urllib.urlencode(parameters),
                        urllib.urlencode(parameters),
                        {'Content-Type' : 'application/x-www-form-urlencoded'}
                    )
                response = connection.getresponse()
                file = StringIO.StringIO(response.read())
                
                if response.status == 200:
                    csv.field_size_limit(1000000000)
                    
                    count = 0
                    keys = []
                    data = []
                    for row in csv.reader(file):
                        if len(keys) <= 0:
                            keys = row
                        else:
                            tmp = {}
                            for i in range(len(row)):
                                tmp[keys[i]] = row[i]
                            count += 1
                            data.append(tmp)
                    
                    output['count'] = count
                    output['data'] = data
                    
                    success = True
                else:
                    success = False
                    output['error'] = [file.getvalue()]    
            except Exception as e:
                logging.error(e)
                success = False
                output['error'] = ['Bad input parameters.']
        else:
            success = False
            output['error'] = ['Missing sql parameter.']
        
        output['success'] = success
        
        self.set_header('Access-Control-Allow-Origin', '*')
        
        jsonp = self.get_argument('jsonp', '')
        if jsonp != '':
            self.set_header('Content-Type', 'text/javascript')
            self.write(jsonp + '(' + json.dumps(output) + ');')
        else:
            self.set_header('Content-Type', 'application/json')
            self.write(json.dumps(output))
    
    def post(self):
        self.get()