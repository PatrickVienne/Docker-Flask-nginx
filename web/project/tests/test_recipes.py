# project/test_recipes.py


import os
import unittest

from project import app, db, mail
from project.models import Recipe, User


TEST_DB = 'test.db'


class RecipesTests(unittest.TestCase):

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

    def register(self, email, password, confirm):
        return self.app.post(
            '/register',
            data=dict(email=email, password=password, confirm=confirm),
            follow_redirects=True
        )

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

    def test_main_page(self):
        self.register_user()
        self.add_recipes()
        self.logout_user()
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Kennedy Family Recipes', response.data)
        self.assertIn(b'Register', response.data)
        self.assertIn(b'Hamburgers', response.data)
        self.assertIn(b'Mediterranean Chicken', response.data)
        self.assertNotIn(b'Tacos', response.data)
        self.assertNotIn(b'Homemade Pizza', response.data)

    def test_user_recipes_page(self):
        self.register_user()
        self.add_recipes()
        response = self.app.get('/recipes', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Kennedy Family Recipes', response.data)
        self.assertIn(b'Hamburgers', response.data)
        self.assertIn(b'Mediterranean Chicken', response.data)
        self.assertIn(b'Tacos', response.data)
        self.assertIn(b'Homemade Pizza', response.data)

    def test_user_recipes_page_without_login(self):
        response = self.app.get('/recipes', follow_redirects=False)
        self.assertEqual(response.status_code, 302)
        self.assertIn(b'You should be redirected automatically to target URL:', response.data)
        self.assertIn(b'/login?next=%2Frecipes', response.data)

    def test_add_recipe_page(self):
        self.register_user()
        response = self.app.get('/add', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Add a New Recipe', response.data)

    def test_add_recipe(self):
        self.register_user()
        response = self.app.post(
            '/add',
            data=dict(recipe_title='Hamburgers2',
                      recipe_description='Delicious hamburger with pretzel rolls'),
            follow_redirects=True)
        self.assertIn(b'New recipe, Hamburgers2, added!', response.data)

    def test_add_invalid_recipe(self):
        self.register_user()
        response = self.app.post(
            '/add',
            data=dict(recipe_title='',
                      recipe_description='Delicious hamburger with pretzel rolls'),
            follow_redirects=True)
        self.assertIn(b'ERROR! Recipe was not added.', response.data)
        self.assertIn(b'This field is required.', response.data)

    def test_recipe_detail_public_recipe(self):
        self.register_user()
        self.add_recipes()
        self.logout_user()
        response = self.app.get('/recipe/1', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Hamburgers', response.data)
        self.assertIn(b'Public', response.data)
        self.assertIn(b'patkennedy79@gmail.com', response.data)

    def test_recipe_detail_private_recipe(self):
        self.register_user()
        self.add_recipes()
        response = self.app.get('/recipe/3', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Tacos', response.data)
        self.assertIn(b'Private', response.data)
        self.assertIn(b'patkennedy79@gmail.com', response.data)

    def test_recipe_detail_private_recipe_invalid_user(self):
        self.register_user()
        self.add_recipes()
        self.logout_user()
        response = self.app.get('/recipe/3', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Error! Incorrect permissions to access this recipe.', response.data)

if __name__ == "__main__":
    unittest.main()
