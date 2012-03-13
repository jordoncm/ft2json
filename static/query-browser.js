var authData = null;

function init() {
    initAuth();
}

function initAuth() {
    if(typeof window.location.hash != 'undefined' && window.location.hash !== '') {
        authData = {};
        var tmp = window.location.hash.split('&');
        var tmp2 = null;
        for(var i = 0; i < tmp.length; i++) {
            tmp2 = tmp[i].split('=');
            if(tmp2[0].indexOf('#') === 0) {
                tmp2[0] = tmp2[0].substr(1);
            }
            authData[tmp2[0]] = tmp2[1];
        }
        
        document.getElementById('token').value = authData.access_token;
    }
}

function execute() {
    var query = document.getElementById('query').value;
    query = query.replace(/[\r\t\n]/g, ' ');
    
    if(query != '') {
        var parameters = {};
        if(authData && typeof authData.access_token != 'undefined') {
            parameters = {access_token : authData.access_token};
        }
        ft2json.query(query , response, parameters);
    }
}

function response(result) {
    if(result.success == true) {
        document.getElementById('status').style.color = '#00CC00';
        document.getElementById('status').innerHTML = 'SUCCESS';
        
        var html = [
            '<table class="result">'
        ];
        for(var i = 0; i < result.data.length; i++) {
            var row = result.data[i];
            
            if(i == 0) {
                html.push('<thead>');
                html.push('<tr>');
                for(var j in row) {
                    html.push('<th>' + j + '</th>');
                }
                html.push('</tr>');
                html.push('</thead>');
                
                html.push('<tbody>');
            }
            
            html.push('<tr>');
            for(var k in row) {
                html.push('<td>' + row[k] + '</td>');
            }
            html.push('</tr>');
        }
        html.push('</tbody>');
        html.push('</table>');
        
        document.getElementById('response').innerHTML = html.join('');
    } else {
        document.getElementById('status').style.color = '#CC0000';
        document.getElementById('status').innerHTML = 'FAILED';
        document.getElementById('response').innerHTML = '<div class="error">' + result.error[0] + '</div>';
    }
}

function clearQuery() {
    document.getElementById('query').value = '';
    document.getElementById('status').innerHTML = '';
    document.getElementById('response').innerHTML = '';
}

function authenticate() {
    window.location = 'https://accounts.google.com/o/oauth2/auth?' + 
        'response_type=token&client_id=318699904972.apps.googleusercontent.com&scope=' + 
        encodeURIComponent('https://www.googleapis.com/auth/fusiontables') + 
        '&redirect_uri=' + 
        encodeURIComponent(window.location.protocol + '//' + window.location.host + window.location.pathname);
}

function csv() {
    var query = document.getElementById('query').value;
    query = query.replace(/[\r\t\n]/g, ' ');
    
    if(query != '') {
        var qs = '';
        if(authData && typeof authData.access_token != 'undefined') {
            qs = '&access_token=' + authData.access_token;
        }
        window.location = 'https://www.google.com/fusiontables/api/query?sql=' + encodeURIComponent(query) + qs;
    }
}

function json() {
    var query = document.getElementById('query').value;
    query = query.replace(/[\r\t\n]/g, ' ');
    
    if(query != '') {
        var qs = '';
        if(authData && typeof authData.access_token != 'undefined') {
            qs = '&access_token=' + authData.access_token;
        }
        window.location = '/q?sql=' + encodeURIComponent(query) + qs;
    }
}