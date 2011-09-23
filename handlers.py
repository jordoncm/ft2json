import csv
import json
import StringIO
import tornado.web
import urllib
import urllib2

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
            # try:
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
            try:
                parameters = {
                    'sql' : sql
                }
                accessToken = self.get_argument('access_token', '')
                if accessToken != '':
                    parameters['access_token'] = accessToken
                if method == 'get':
                    request = urllib2.Request(
                        'https://www.google.com/fusiontables/api/query?' + urllib.urlencode(parameters)
                    )
                elif method == 'post':
                    request = urllib2.Request(
                        'https://www.google.com/fusiontables/api/query',
                        urllib.urlencode(parameters),
                        {'Content-Type' : 'application/x-www-form-urlencoded'}
                    )
                response = urllib2.urlopen(request)
                file = StringIO.StringIO(response.read())
            except urllib2.HTTPError, e:
                file = StringIO.StringIO(e.read())
                self.write(file.getvalue())
            
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
            # except:
            #     success = False
        else:
            success = False
        
        output['success'] = success
        
        self.write(json.dumps(output))
    
    def post(self):
        self.get()