import csv
import httplib
try:
    import json
except ImportError:
    from django.utils import simplejson as json
import StringIO
import tornado.web
import urllib

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.set_header('Content-Type', 'application/json')
        
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
                
                connection = httplib.HTTPSConnection('www.google.com')
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
            except:
                success = False
                output['error'] = ['Bad input parameters.']
        else:
            success = False
            output['error'] = ['Missing sql parameter.']
        
        output['success'] = success
        
        self.write(json.dumps(output))
    
    def post(self):
        self.get()