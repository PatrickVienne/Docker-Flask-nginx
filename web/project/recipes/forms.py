# project/recipes/forms.py


from flask_wtf import Form
from wtforms import StringField, BooleanField, RadioField, IntegerField
from wtforms.validators import DataRequired, NumberRange
from flask_wtf.file import FileField, FileAllowed, FileRequired
from flask_pagedown.fields import PageDownField
from project import images


class AddRecipeForm(Form):
    recipe_title = StringField('Recipe Title', validators=[DataRequired()])
    recipe_description = StringField('Recipe Description', validators=[DataRequired()])
    recipe_public = BooleanField('Public Recipe', default="")
    recipe_type = RadioField('Recipe Type', validators=[DataRequired()],
                             choices=[('Breakfast', 'Breakfast Recipe'),
                                      ('Lunch', 'Lunch Recipe'),
                                      ('Dinner', 'Dinner Recipe'),
                                      ('Dessert', 'Dessert Recipe'),
                                      ('Side', 'Side Dish')],
                             default='Dinner')
    recipe_rating = IntegerField('Recipe Rating', validators=[NumberRange(min=1, max=5, message='Rating must be between 1 and 5!')])
    recipe_image = FileField('Recipe Image', validators=[FileRequired(), FileAllowed(images, 'Images only!')])
    recipe_ingredients = PageDownField('Recipe Ingredients', validators=[DataRequired()], render_kw={"rows": 12, "cols": 100})
    recipe_steps = PageDownField('Recipe Steps', validators=[DataRequired()], render_kw={"rows": 12, "cols": 100})


class EditRecipeForm(Form):
    recipe_title = StringField('Recipe Title', validators=[])
    recipe_description = StringField('Recipe Description', validators=[])
    recipe_public = BooleanField('Public Recipe', default="")
    recipe_type = RadioField('Recipe Type', validators=[],
                             choices=[('Breakfast', 'Breakfast Recipe'),
                                      ('Lunch', 'Lunch Recipe'),
                                      ('Dinner', 'Dinner Recipe'),
                                      ('Dessert', 'Dessert Recipe'),
                                      ('Side', 'Side Dish')],
                             default='Dinner')
    recipe_rating = IntegerField('Recipe Rating', validators=[])
    recipe_image = FileField('Recipe Image', validators=[FileAllowed(images, 'Images only!')])
    recipe_ingredients = PageDownField('Recipe Ingredients', validators=[], render_kw={"rows": 12, "cols": 100})
    recipe_steps = PageDownField('Recipe Steps', validators=[], render_kw={"rows": 12, "cols": 100})
