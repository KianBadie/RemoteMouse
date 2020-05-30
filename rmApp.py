def app(environ, start_response):
    """
    A barebones WSGI application.
    This is a starting point for your own Web framework :)
    """

    # For now, return empty response for favicon.io
    if environ['PATH_INFO'] == '/favicon.ico': return []

    status = '200 OK'

    # Construct Headers
    if environ['PATH_INFO'] == '/':
        response_headers = [('Content-Type', 'text/html')]
    else:
        file_type = environ['PATH_INFO'].split('.', 1)[1]
        response_headers = [('Content-Type', f'text/{file_type}')]

    # Get page path
    page = 'error.html'
    if environ['PATH_INFO'] == '/':
        page = 'index.html'
    else:
        page = environ['PATH_INFO'][1:]

    start_response(status, response_headers)
    response = []
    with open(page, 'r+b') as page:
        response.append(page.read())
    return response