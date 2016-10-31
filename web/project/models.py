from project import db, bcrypt
from sqlalchemy.ext.hybrid import hybrid_method, hybrid_property
from datetime import datetime
from markdown import markdown
import bleach


# Allowable HTML tags
allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code',
                'em', 'i', 'li', 'ol', 'pre', 'strong', 'ul',
                'h1', 'h2', 'h3', 'p']


class Recipe(db.Model):
    """Recipe fields to add:
        date created
        date last modified
    """
    __tablename__ = "recipes"

    id = db.Column(db.Integer, primary_key=True)
    recipe_title = db.Column(db.String, nullable=False)
    recipe_description = db.Column(db.String, nullable=False)
    is_public = db.Column(db.Boolean, nullable=False)
    image_filename = db.Column(db.String, default=None, nullable=True)
    image_url = db.Column(db.String, default=None, nullable=True)
    recipe_type = db.Column(db.String, default=None, nullable=True)
    rating = db.Column(db.Integer, default=None, nullable=True)
    ingredients = db.Column(db.Text, default=None, nullable=True)
    ingredients_html = db.Column(db.Text, default=None, nullable=True)
    recipe_steps = db.Column(db.Text, default=None, nullable=True)
    recipe_steps_html = db.Column(db.Text, default=None, nullable=True)
    inspiration = db.Column(db.String, default=None, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, title, description, user_id, is_public, image_filename=None, image_url=None, recipe_type=None,
                 rating=None, ingredients=None, recipe_steps=None, inspiration=None):
        self.recipe_title = title
        self.recipe_description = description
        self.is_public = is_public
        self.image_filename = image_filename
        self.image_url = image_url
        self.recipe_type = recipe_type
        self.rating = rating
        self.ingredients = ingredients
        self.recipe_steps = recipe_steps
        self.inspiration = inspiration
        self.user_id = user_id

    def __repr__(self):
        return '<id: {}, title: {}, user_id: {}>'.format(self.id, self.recipe_title, self.user_id)

    @staticmethod
    def on_changed_ingredients(target, value, oldvalue, iterator):
        if value:
            target.ingredients_html = bleach.linkify(bleach.clean(markdown(value, output_format='html'),
                                                                  tags=allowed_tags, strip=True))

    @staticmethod
    def on_changed_recipe_steps(target, value, oldvalue, iterator):
        if value:
            target.recipe_steps_html = bleach.linkify(bleach.clean(markdown(value, output_format='html'),
                                                                   tags=allowed_tags, strip=True))

db.event.listen(Recipe.ingredients, 'set', Recipe.on_changed_ingredients)
db.event.listen(Recipe.recipe_steps, 'set', Recipe.on_changed_recipe_steps)


class User(db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String, unique=True, nullable=False)
    _password = db.Column(db.Binary(60), nullable=False)
    authenticated = db.Column(db.Boolean, default=False)
    email_confirmation_sent_on = db.Column(db.DateTime, nullable=True)
    email_confirmed = db.Column(db.Boolean, nullable=True, default=False)
    email_confirmed_on = db.Column(db.DateTime, nullable=True)
    registered_on = db.Column(db.DateTime, nullable=True)
    last_logged_in = db.Column(db.DateTime, nullable=True)
    current_logged_in = db.Column(db.DateTime, nullable=True)
    role = db.Column(db.String, default='user')
    recipes = db.relationship('Recipe', backref='user', lazy='dynamic')

    def __init__(self, email, plaintext_password, email_confirmation_sent_on=None, role='user'):
        self.email = email
        self.password = plaintext_password
        self.authenticated = False
        self.email_confirmation_sent_on = email_confirmation_sent_on
        self.email_confirmed = False
        self.email_confirmed_on = None
        self.registered_on = datetime.now()
        self.last_logged_in = None
        self.current_logged_in = datetime.now()
        self.role = role

    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def set_password(self, plaintext_password):
        self._password = bcrypt.generate_password_hash(plaintext_password)

    @hybrid_method
    def is_correct_password(self, plaintext_password):
        return bcrypt.check_password_hash(self.password, plaintext_password)

    @property
    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return self.authenticated

    @property
    def is_active(self):
        """Always True, as all users are active."""
        return True

    @property
    def is_anonymous(self):
        """Always False, as anonymous users aren't supported."""
        return False

    def get_id(self):
        """Return the email address to satisfy Flask-Login's requirements."""
        """Requires use of Python 3"""
        return str(self.id)

    def __repr__(self):
        return '<User {}>'.format(self.email)

