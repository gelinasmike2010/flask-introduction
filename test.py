# The big picture in unit testing:

# Unit testing is a method of determining the correctness individual functions
# isolated from a larger codebase. The idea is that if all the atomic units of
# an application work as intended in isolation, then integrating them together
# as intended is much easier. This aids greatly in isolating bugs.

# -----------------------------------------------------------------------------

# Best practices in unit testing:

# Each unit test should focus on one tiny bit of functionality and prove it correct
# Each test must be able to run alone
# Tests will output their runtime. Make the tests run fast.
# Use long and descriptive names for testing functions. Start each test name with "test"
# Test by plugging in a correct or incorrect input; then see if the response is as expected

# -----------------------------------------------------------------------------

# An example test using the unittest library:

# import unittest
#
# def func(x):
#     return x + 1
#
# class MyTest(unittest.TestCase):
#     def test(self):
#         self.assertEqual(func(3), 4)

# ----------------------------------------------

from app import app
import unittest

class FlaskTestCase(unittest.TestCase):

    # Ensure Flask was set up correctly by checking for a successful HTTP response
    def test_index(self):
        tester = app.test_client(self)
        response = tester.get('/login', content_type='html/text') # tester.get accesses the route (arg 1)
        self.assertEqual(response.status_code, 200)

    # Ensure the login page loads correctly by checking that 'Please Login' is shown
    def test_login_page_loads(self):
        tester = app.test_client(self)
        response = tester.get('/login', content_type='html/text')
        self.assertTrue(b'Please Log In' in response.data)

    # Ensure log in occurs wtih correct credentialing by checking for
    # our response to the correct username/password combination as seen in app.login
    def test_correct_login(self):
        tester = app.test_client(self)
        response = tester.post(
            '/login',
            data=dict(username="admin", password="admin"),
            follow_redirects=True
        )
        self.assertIn(b'You are logged in.', response.data)

    # Ensure log in fails with incorrect credentials
    def test_incorrect_login(self):
        tester = app.test_client(self)
        response = tester.post(
            '/login',
            data=dict(username="wrong_username", password="wrong_password"),
            follow_redirects=True
        )
        self.assertIn(b'Invalid credentials. Please try again.', response.data)

    # Ensure log out occurs when clicked
    def test_logout(self):
        tester = app.test_client(self)
        # to test logout, we need our test client to be logged in!
        response = tester.post(
            '/login',
            data=dict(username="admin", password="admin"),
            follow_redirects=True
        )
        response = tester.get('/logout', follow_redirects=True)
        self.assertTrue(b'You are logged out.' in response.data)

    # Ensure that the main page requires a login
    def test_main_page_requires_login(self):
        tester = app.test_client(self)
        response = tester.get('/', follow_redirects=True)
        self.assertTrue(b'You need to log in first.' in response.data)

    # Ensure that the logout page requires a login
    def test_logout_route_requires_login(self):
        tester = app.test_client(self)
        response = tester.get('/logout', follow_redirects=True)
        self.assertTrue(b'You need to log in first.' in response.data)

    # Ensure that posts show up on the main page - must be logged in!
    def test_posts_appear_on_main_page(self):
        tester = app.test_client(self)
        response = tester.post(
            '/login',
            data=dict(username="admin", password="admin"),
            follow_redirects=True
        )
        self.assertIn(b'Good', response.data)

if __name__ == '__main__':
    unittest.main()
