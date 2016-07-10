# project/test_users.py


import os
import unittest

from project import app, db


TEST_DB = 'user.db'


class UsersTests(unittest.TestCase):

    ############################
    #### setup and teardown ####
    ############################

    # executed prior to each test
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
            os.path.join(app.config['BASEDIR'], TEST_DB)
        self.app = app.test_client()
        db.drop_all()
        db.create_all()

        self.assertEquals(app.debug, False)

    # executed after each test
    def tearDown(self):
        pass


    ########################
    #### helper methods ####
    ########################

    def register(self, email, password, confirm):
        return self.app.post(
            '/register',
            data=dict(email=email, password=password, confirm=confirm),
            follow_redirects=True
        )


    ###############
    #### tests ####
    ###############

    def test_login_page(self):
        response = self.app.get('/login', follow_redirects=True)
        self.assertIn(b'Future site for logging into Kennedy Family Recipes!', response.data)

    def test_user_registration_form_displays(self):
        response = self.app.get('/register')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Please Register Your New Account', response.data)

    def test_valid_user_registration(self):
        self.app.get('/register', follow_redirects=True)
        response = self.register('patkennedy79@gmail.com', 'FlaskIsAwesome', 'FlaskIsAwesome')
        self.assertIn(b'Thanks for registering!', response.data)

    def test_duplicate_email_user_registration_error(self):
        self.app.get('/register', follow_redirects=True)
        self.register('patkennedy79@yahoo.com', 'FlaskIsAwesome', 'FlaskIsAwesome')
        self.app.get('/register', follow_redirects=True)
        response = self.register('patkennedy79@yahoo.com', 'FlaskIsReallyAwesome', 'FlaskIsReallyAwesome')
        self.assertIn(b'ERROR! Email (patkennedy79@yahoo.com) already exists.', response.data)

    def test_missing_field_user_registration_error(self):
        self.app.get('/register', follow_redirects=True)
        response = self.register('patkennedy79@gmail.com', 'FlaskIsAwesome', '')
        self.assertIn(b'This field is required.', response.data)


if __name__ == "__main__":
    unittest.main()
