var ft2json = {};
ft2json.callbacks = {};

ft2json.query = function(sql, callback, parameters) {
    if(sql && sql != '' && callback) {
        if(!parameters) {
            parameters = {};
        }
        
        parameters.sql = sql;
        
        var src = 'http://ft2json.appspot.com/q/?sql=' + encodeURIComponent(parameters.sql);
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
}