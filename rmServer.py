import socket
import sys
import datetime
import io
from hashlib import sha1
from base64 import b64encode

from request import Request

PORT = int(sys.argv[2])
HOST = sys.argv[3]
ADDRESS = (HOST, PORT)

class Server():

    address_family = socket.AF_INET
    socket_type = socket.SOCK_STREAM

    def __init__(self, server_address, app):
       """
       Parameters
       ----------
       server_address : tuple
            ( HOST, PORT )
       application : WSGI application
            An application that works with WSGI
       """ 
       self.server_address = server_address
       self.listen_socket = socket.socket(self.address_family, self.socket_type)
       self.listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
       self.listen_socket.bind(server_address)
       self.listen_socket.listen()
       self.app = app
       # Return headers set by Web framework/Web application
       self.headers_set = []
    
    def serve_forever(self):
        print('Listening on %s:%s' % self.server_address)
        while True:
            client_connection, client_address = self.listen_socket.accept()
            self.handle_request(client_connection)
    
    def handle_request(self, client_connection):
        request_data = client_connection.recv(1024).decode('utf-8')
        print(request_data)

        request_parsed = Request(request_data)
        if 'Upgrade' in request_parsed.headers:
            key = self.get_websocket_key(request_parsed)
            status = '101 Switching Protocols'
            response_headers = [('Sec-WebSocket-Accept', key), ('Upgrade', 'websocket'), ('Connection', 'Upgrade')]
            self.start_response(status, response_headers)
            self.finish_response([b'Test message'], client_connection)
        else:
            # Construct environment dictionary using request data
            env = self.get_environ(request_parsed.request, request_data)
            result = self.app(env, self.start_response)
            self.finish_response(result, client_connection)

    def parse_request(self, request_data):
        request_line = request_data.splitlines()[0]
        return tuple(request_line.split())
    
    def get_environ(self, request, request_data):
        env = {}
        # The following code snippet does not follow PEP8 conventions
        # but it's formatted the way it is for demonstration purposes
        # to emphasize the required variables and their values
        #
        # Required WSGI variables
        env['wsgi.version']      = (1, 0)
        env['wsgi.url_scheme']   = 'http'
        env['wsgi.input']        = io.StringIO(request_data)
        env['wsgi.errors']       = sys.stderr
        env['wsgi.multithread']  = False
        env['wsgi.multiprocess'] = False
        env['wsgi.run_once']     = False
        # Required CGI variables
        env['REQUEST_METHOD']    = request['method']
        env['PATH_INFO']         = request['path']
        env['SERVER_NAME']       = self.server_address[0]
        env['SERVER_PORT']       = str(self.server_address[1])
        return env
    
    def start_response(self, status, response_headers):
        server_headers = [
            ('Date', str(datetime.datetime.now())),
            ('Server', 'rmServer'),
        ]
        self.headers_set = [status, response_headers + server_headers]

    def finish_response(self, result, client_connection):
        try:
            status, response_headers = self.headers_set
            response = f'HTTP/1.1 {status}\r\n'
            for header in response_headers:
                response += '{0}: {1}\r\n'.format(*header)
            response += '\r\n'
            for data in result:
                response += data.decode('utf-8')
            response_bytes = response.encode()
            client_connection.sendall(response_bytes)
        finally:
            client_connection.close()
    
    def get_websocket_key(self, request_parsed):
        magic_string = '258EAFA5-E914-47DA-95CA-C5AB0DC85B11'
        websocket_key = sha1()
        websocket_key.update(bytes(request_parsed.headers['Sec-WebSocket-Key'] + magic_string, 'utf-8'))
        return b64encode(websocket_key.digest()).decode()

    def shut_down(self):
        print('\nClosing connection on %s:%s\n' % self.server_address)
        self.listen_socket.close()

app_path = sys.argv[1]
module, application = app_path.split(':')
module = __import__(module)
application = getattr(module, application)
rmServer = Server(ADDRESS, application)
try:
    rmServer.serve_forever()
finally:
    rmServer.shut_down()
