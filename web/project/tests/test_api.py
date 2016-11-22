# project/test_api.py


import os
import unittest
import json
from io import BytesIO


from project import app, db, mail
from project.models import Recipe, User


TEST_DB = 'test.db'
# URL_BASE = 'http://192.168.99.100/'
URL_BASE = 'http://localhost:5000/'


class ApiTests(unittest.TestCase):

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

        mail.init_app(app)
        self.assertEquals(app.debug, False)

    # executed after each test
    def tearDown(self):
        pass


    ########################
    #### helper methods ####
    ########################

    @staticmethod
    def register2(test_client, email, password, confirm_password):
        return test_client.post('/register',
                                data=dict(email=email,
                                          password=password,
                                          confirm=confirm_password),
                                follow_redirects=True)

    def register(self, email, password, confirm):
        return self.app.post(
            '/register',
            data=dict(email=email, password=password, confirm=confirm),
            follow_redirects=True
        )

    @staticmethod
    def login2(test_client, email, password):
        return test_client.post('/login',
                                data=dict(email=email, password=password),
                                follow_redirects=True)

    def login(self, email, password):
        return self.app.post(
            '/login',
            data=dict(email=email, password=password),
            follow_redirects=True
        )

    def register_user(self):
        self.app.get('/register', follow_redirects=True)
        self.register('patkennedy79@gmail.com', 'FlaskIsAwesome', 'FlaskIsAwesome')

    def login_user(self):
        self.app.get('/login', follow_redirects=True)
        self.login('patkennedy79@gmail.com', 'FlaskIsAwesome')

    def logout_user(self):
        self.app.get('/logout', follow_redirects=True)

    @staticmethod
    def add_recipes2():
        user1 = User.query.filter_by(email='patkennedy79@gmail.com').first()
        recipe1 = Recipe('Hamburgers', 'Classic dish elevated with pretzel buns.', user1.id, True)
        recipe2 = Recipe('Mediterranean Chicken', 'Grilled chicken served with pitas, hummus, and sauted vegetables.', user1.id, True)
        recipe3 = Recipe('Tacos', 'Ground beef tacos with grilled peppers.', user1.id, False)
        recipe4 = Recipe('Homemade Pizza', 'Homemade pizza made using pizza oven', user1.id, False)
        db.session.add(recipe1)
        db.session.add(recipe2)
        db.session.add(recipe3)
        db.session.add(recipe4)
        db.session.commit()


    def add_recipes(self):
        self.register_user()
        user1 = User.query.filter_by(email='patkennedy79@gmail.com').first()
        recipe1 = Recipe('Hamburgers', 'Classic dish elevated with pretzel buns.', user1.id, True)
        recipe2 = Recipe('Mediterranean Chicken', 'Grilled chicken served with pitas, hummus, and sauted vegetables.', user1.id, True)
        recipe3 = Recipe('Tacos', 'Ground beef tacos with grilled peppers.', user1.id, False)
        recipe4 = Recipe('Homemade Pizza', 'Homemade pizza made using pizza oven', user1.id, False)
        db.session.add(recipe1)
        db.session.add(recipe2)
        db.session.add(recipe3)
        db.session.add(recipe4)
        db.session.commit()


    ###############
    #### tests ####
    ###############

    def test_api_get_all_recipes(self):
        app_client = app.test_client()
        self.register2(app_client, 'patkennedy79@gmail.com', 'FlaskIsAwesome', 'FlaskIsAwesome')
        self.add_recipes2()

        response = app_client.get('/api/v1_1/recipes')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Hamburgers', response.data)
        self.assertIn(b'Classic dish elevated with pretzel buns.', response.data)
        self.assertIn(b'Mediterranean Chicken', response.data)
        self.assertIn(b'Grilled chicken served with pitas, hummus, and sauted vegetables.', response.data)
        self.assertIn(b'Tacos', response.data)
        self.assertIn(b'Ground beef tacos with grilled peppers.', response.data)
        self.assertIn(b'Homemade Pizza', response.data)
        self.assertIn(b'Homemade pizza made using pizza oven', response.data)

    def test_api_get_recipe(self):
        app_client = app.test_client()
        self.register2(app_client, 'patkennedy79@gmail.com', 'FlaskIsAwesome', 'FlaskIsAwesome')
        self.add_recipes2()

        response = app_client.get('/api/v1_1/recipes/1')
        print('Retrieving recipe #1...')
        print('\tstatus: {}'.format(response.status))
        print('\tdata: {}'.format(response.data))
        print('\tjson: {}',format(response.json))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Hamburgers', response.data)
        self.assertIn(b'Classic dish elevated with pretzel buns.', response.data)

        response = app_client.get('/api/v1_1/recipes/2')
        print('Retrieving recipe #2...')
        print('\tstatus: {}'.format(response.status))
        print('\tdata: {}'.format(response.data))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Mediterranean Chicken', response.data)
        self.assertIn(b'Grilled chicken served with pitas, hummus, and sauted vegetables.', response.data)

        response = app_client.get('/api/v1_1/recipes/5')
        print('Retrieving recipe #5...')
        print('\tstatus: {}'.format(response.status))
        print('\tdata: {}'.format(response.data))
        self.assertEqual(response.status_code, 404)
        self.assertIn(b'error', response.data)
        self.assertIn(b'Not found', response.data)

    def test_api_add_recipe(self):
        app_client = app.test_client()
        self.register2(app_client, 'patkennedy79@gmail.com', 'FlaskIsAwesome', 'FlaskIsAwesome')
        self.add_recipes2()

        # TEMPORARY: Using v1.0 of the Rest API
        response = app_client.post('/api/v1_0/recipes',
                                   buffered=True,
                                   content_type='multipart/form-data',
                                   data=json.dumps({'title': 'Hamburgers2',
                                                    'description': 'Delicious hamburger with pretzel rolls',
                                                    'recipe_type': 'Dinner',
                                                    'recipe_steps': 'Step 1 Step 2 Step 3',
                                                    'recipe_ingredients': 'Ingredient #1 Ingredient #2',
                                                    'recipe_inspiration': 'http://www.foodnetwork.com/blaa'}),
                                   follow_redirects=True)
        print('Adding a new recipe...')
        print('\tstatus: {}'.format(response.status))
        print('\tdata: {}'.format(response.data))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Hamburgers2', response.data)

    def test_api_delete_recipe(self):
        app_client = app.test_client()
        self.register2(app_client, 'patkennedy79@gmail.com', 'FlaskIsAwesome', 'FlaskIsAwesome')
        self.add_recipes2()

        response = app_client.delete('/api/v1_1/recipes/2')
        print('Deleting recipe #2...')
        print('\tstatus: {}'.format(response.status))
        print('\tdata: {}'.format(response.data))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'true', response.data)

    def test_api_update_recipe(self):
        app_client = app.test_client()
        self.register2(app_client, 'patkennedy79@gmail.com', 'FlaskIsAwesome', 'FlaskIsAwesome')
        self.add_recipes2()

        response = app_client.put('/api/v1_1/recipes/3',
                                  data={'title': '3Tacos3',
                                        'description': '3Tacos are delicious3'},
                                  json={'title': '3Tacos3',
                                        'description': '3Tacos are delicious3'},
                                  follow_redirects=True)
        print('Updating recipe #3...')
        print('\tstatus: {}'.format(response.status))
        print('\tdata: {}'.format(response.data))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'3Tacos3', response.data)
        self.assertIn(b'3Tacos are delicious3', response.data)


if __name__ == "__main__":
    unittest.main()
