# import flask

# @app.route('/')
# def index():
#     return 'index'

# @app.route('/login')
# def login():
#     return 'login'

# @app.route('/user/<username>')
# def profile(username):
#     return f"{username}'s profile"

# with app.test_request_context():
#     print(flask.url_for('index'))
#     print(flask.url_for('login'))
#     print(flask.url_for('login', next='/'))
#     print(flask.url_for('profile', username='John Doe'))