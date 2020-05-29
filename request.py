class Request():

    def __init__(self, request_data):
        request_lines = request_data.splitlines()
        request_tuple = request_lines[0].split()
        self.request = {
            'method': request_tuple[0],
            'path': request_tuple[1],
            'version': request_tuple[2]
        }
        self.headers = dict()
        for i in range(1, len(request_lines) - 1):
            header, value = request_lines[i].split(':', 1)
            header = header.rstrip(':')
            value = value.strip()
            self.headers[header] = value