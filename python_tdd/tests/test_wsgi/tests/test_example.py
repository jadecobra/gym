import wsgiref.util
import wsgiref.simple_server


# A Relatively simple WSGI application.
# It's going to print out the environment dictionary after being updated by setup_testing_defaults
def simple_app(environ, start_response):
    wsgiref.util.setup_testing_defaults(environ)

    status = '200 OK'
    headers = [('Content-type', 'text/plain; charset=utf-8')]

    start_response(status, headers)

    return [f"{key}: {value}\n".encode('utf-8') for key, value in environ.items()]

with wsgiref.simple_server.make_server('', 8000, simple_app) as httpd:
    print('Serving on port 8000...')
    httpd.serve_forever()