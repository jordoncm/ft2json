/**
 * Copyright 2012 Jordon Mears (http://www.finefrog.com/)
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

var ft2json = {};
ft2json.callbacks = {};

ft2json.query = function(sql, callback, parameters) {
    if(sql && sql !== '' && callback) {
        if(!parameters) {
            parameters = {};
        }
        
        parameters.sql = sql;
        
        var host = (window.location.port == '80' || window.location.port == '443' || window.location.port == '') ? window.location.hostname : window.location.hostname + ':' + window.location.port;
        var src = window.location.protocol + '//' + host + '/q/?sql=' + encodeURIComponent(parameters.sql);
        var i = null;
        for(i in parameters) {
            src += '&' + encodeURIComponent(i) + '=' + encodeURIComponent(parameters[i]);
        }
        
        var hash = ft2json.generateHash();
        ft2json.callbacks[hash] = {
            apiCallback : callback,
            handler : function(json) {
                ft2json.callbacks[hash].apiCallback(json);
                delete ft2json.callbacks[hash];
            }
        };
        
        src += '&jsonp=' + encodeURIComponent('ft2json.callbacks.' + hash + '.handler');
        
        var head = document.getElementsByTagName('head').item(0);
        var script = document.createElement('script');
        script.type = 'text/javascript';
        script.src = src;
        
        head.appendChild(script);
    }
};

ft2json.generateHash = function() {
    var text = '';
    var possible = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz';

    for(var i = 0; i < 5; i++) {
        text += possible.charAt(Math.floor(Math.random() * possible.length));
    }
    
    return text;
};