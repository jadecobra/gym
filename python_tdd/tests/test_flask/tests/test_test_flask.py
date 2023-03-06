import unittest
import pathlib
import flask
import click


class TestSendingRequests(unittest.TestCase):

    @unittest.skip
    def test_request_example(self):
        response = client.get('/posts')
        self.assertIn(b"<h2>Hello, World!</h2>", response.data)


class TestFormData(unittest.TestCase):
    @unittest.skip
    def test_edit_user(self):
        resources = pathlib.Path(__file__).parent / 'resources'
        response = client.post(
            "/user/2/edit", data={
                "name": "Flask",
                "theme": "dark",
                "picture": (resources / "picture.png").open("rb"),
            }
        )
        self.assertEqual(response.status_code, 200)



class TestJsonData(unittest.TestCase):

    @unittest.skip
    def test_json_data(self):
        response = client.post(
            "/graphql",
            json={
                "query": """
                    query User($id: String!) {
                        user(id: $id) {
                            name
                            theme
                            picture_url
                        }
                    }
                """,
            },
            variables={"id", 2},
        )
        self.assertEqual(response.json['data']['user']['name'], 'Flask')


class TestFollowingRedirects(unittest.TestCase):

    @unittest.skip
    def test_logout_redirect(self):
        response = client.get("/logout")
        # Check that there was one redirect response
        self.assertEqual(len(response.history), 1)
        # Check that the second request was to the index page
        self.assertEqual(response.request.path, '/index')


class TestAccessingModifyingSession(unittest.TestCase):

    @unittest.skip
    def test_access_session(self):
        with client:
            client.post('/auth/login', data={'username': 'flask'})
            # session is still accessible
            self.assertEqual(flask.session['user_id'], 1)

        # session is no longer accessible
        self.assertEqual(flask.session['user_id'], 1)

    @unittest.skip
    def test_modify_session(self):
        with client.session_transaction() as session:
            # set a user id without going through the login route
            session['user_id'] = 1

        # session is saved now
        response = client.get('/users/me')
        self.assertEqual(response.json['username'], 'flask')


# @unittest.skip
# class TestRunningCommandsWithCliRunner(unittest.TestCase):

#     @app.cli.command('hello')
#     @click.option('--name', default='World')
#     def hello_command(name):
#         click.echo(f'Hello, {name}!')

#     def test_hello_command(self):
#         result = runner.invoke(args='hello')
#         self.assertIn('World', result.output)

#         result = runner.invoke(args=['hello', '--name', 'Flask'])
#         self.assertIn('Flask', result.output)


class TestActiveContext(unittest.TestCase):

    @unittest.skip
    def test_db_post_model(self):
        with app.app_context():
            post = db.session.query(Post).get(1)

    @unittest.skip
    def test_validate_user_edit(self):
        with app.test_request_context(
            '/user/2/edit',
            method='POST',
            data={'name': ''}
        ):
            # call a function that accesses `request`
            messages = validate_edit_user()

        self.assertEqual(message['name'][0], 'Name cannot be empty')

    @unittest.skip
    def test_auth_token(self):
        with app.test_request_context(
            '/user/2/edit',
            headers={'X-Auth-Token': '1'}
        ):
            app.preprocess_request()
            self.assertEqual(g.user.name, 'Flask')