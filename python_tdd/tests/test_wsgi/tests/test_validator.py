import wsgiref.validate
import wsgiref.simple_server

# Our callable object which is intentionally not compliant
# to the standard breaks the validation
def simple_app(environ, start_response):
    status = '200 OK'
    headers = [('Content-type', 'text/plain')]
    start_response(status, headers)

    # This is going to break because we need to return a list,
    # and the validator is going to inform us
    return b'Hello World'

# This is the application wrapped in a validator
validator_app = wsgiref.validate.validator(simple_app)

with wsgiref.simple_server.make_server('', 8000, validator_app) as httpd:
    print('Listening on port 8000...')
    httpd.handle_request()
    # httpd.serve_forever()