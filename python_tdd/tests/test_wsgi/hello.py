'''
Every WSGI application must have an application object
- a callable object that accepts two arguments.
For that purpose, we're going to use a function
(note that you're not limited to a function,
you can use a class for example).
The first argument passed to the function is a dictionary
containing CGI-stype environment variables and the second
variable is the callable object
'''

import wsgiref.simple_server

def app(environ, start_response):
    status = '200 OK' # HTTP Status
    headers = [('Content-type', 'text/plain; charset=utf-8')] # HTTP Headers
    start_response(status, headers)

    # The returned object is going to be printed
    return [b'Hello World']

with wsgiref.simple_server.make_server('', 8000, app) as httpd:
    print('Serving on port 8000...')

    # Serve until process is killed
    httpd.serve_forever()