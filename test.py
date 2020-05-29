import socket

listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
listen_socket.bind(('192.168.254.39', 8000))
listen_socket.listen()
client_connection, client_address = listen_socket.accept()
print('client=', client_connection)
request_data = client_connection.recv(1024).decode('utf-8')
print('request data=', request_data)
listen_socket.shutdown(socket.SHUT_RDWR)
listen_socket.close()