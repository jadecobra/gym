# from flask import request

# with app.test_request_context('/hello', method='POST'):
#     # now you can do something with the request until the
#     # end of the with block, such as basic assertions:
#     assert request.path == '/hello'
#     assert request.method == 'POST'

# with app.request_context(environ):
#     assert request.method == 'POST'