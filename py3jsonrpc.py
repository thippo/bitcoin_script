#Reference: https://github.com/Sourcewerks/bitcoind-jsonrpc3
#Thanks!

import urllib.request
import json
import base64

class _JsonRPCClientProxy():
    
    def __init__(self, url, method, username=None, password=None):
        self.url = url
        self.username = username
        self.password = password
        self.method = method
    
    def __call__(self, *args):
        params = {'method' : self.method, 'params' : args, 'id' : self.method}
        return self._http_request(params)
          
    def _http_request(self, params):
        self.opener = urllib.request.build_opener()
        self.opener.addheaders = [('Content-Type', 'application/json'),
                                  (self._basic_auth(self.username, self.password))]
        data = self._encode_params(params)
        try:
            response = self.opener.open(self.url, data)
        except urllib.error.URLError as e:
            print(e.reason)
            print(e.code)
            print(e.headers)
            
        return json.loads(response.read().decode('utf-8'))
    
    def _encode_params(self, params):
        data = json.dumps(params)
        data = data.encode('utf-8') # data should be bytes
        return data
        
    def _basic_auth(self, username, password):
        encode_string = (username + ':' + password).encode('utf-8')
        base64string = (base64.encodebytes(encode_string)[:-1]).decode('utf-8')
        return ('Authorization', 'Basic ' + base64string)

class JsonRPCClient():
    def __init__(self, url, username=None, password=None):
        self.url = url
        self.username = username
        self.password = password
       
    def __getattr__(self, method):
        return _JsonRPCClientProxy(self.url, method, self.username, self.password)

if __name__ == '__main__':
    jrpc=JsonRPCClient('http://127.0.0.1:8332', 'username', 'password')
    print(jrpc.getinfo())