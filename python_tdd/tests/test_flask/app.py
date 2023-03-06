import flask
import markupsafe

app = flask.Flask(__name__)

@app.route('/')
def index():
    return 'Index Page'

# @app.route('/hello')
# def hello():
#     return 'You Rang?'
@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    return flask.render_template('hello.html', name=name)

@app.route('/user/<username>')
def show_user_profile(username):
    # Show the user profile for that user
    return f'User {markupsafe.escape(username)}'

@app.route('/post/<int:post_id>')
def show_post(post_id):
    # show the post with the given id, the id is an integer
    return f'Post {post_id}'

@app.route('/path/<path:subpath>')
def show_subpath(subpath):
    # show the subpath after /path/
    return f'Subpath {markupsafe.escape(subpath)}'

@app.route('/projects/')
def projects():
    return 'The project page'

@app.route('/about')
def about():
    return 'The about page'

def do_the_login():
    return 'Logging in...'

def show_the_login_form():
    return 'Enter Username and Password'

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if flask.request.method == 'POST':
#         return do_the_login()
#     else:
#         return show_the_login_form()
#     return 'login'

@app.get('/login')
def login_get():
    return show_the_login_form()

@app.get('/login')
def login_post():
    return do_the_login()

@app.route('/user/<username>')
def profile(username):
    return f"{username}'s profile"

with app.test_request_context():
    print(flask.url_for('index'))
    # print(flask.url_for('login'))
    # print(flask.url_for('login', next='/'))
    print(flask.url_for('login_get'))
    print(flask.url_for('login_post'))
    print(flask.url_for('profile', username='John Doe'))
    print(flask.url_for('static', filename='style.css'))

# @app.route('/')
# def hello_world():
    # return '<p>Hello, World!</p>'

# @app.route('/bob')
# def hello_bob():
#     return 'Hello, Bob!'

# @app.route('/boom')
# def hello_boom(arg):
#     return f'Hello {arg}!'

# @app.route('/<name>')
# def hello(name):
#     return f'Hello, {markupsafe.escape(name)}!'