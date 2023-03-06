from flask import request, make_response

@app.route('/')
def index():
    username = request.cookies.get('username')
    # use cookies.get(key) instead of cookies[key] to not get
    # a KeyError if the cookie is missing

# Storing Cookies
@app.route('/')
def index():
    response = make_response(render_template(...))
    response.set_cookie('username', 'the username')
    return response