# project/recipes/views.py

#################
#### imports ####
#################

from flask import render_template, Blueprint, request, redirect, url_for, flash
from flask_login import current_user, login_required
from project import db
from project.models import Recipe, User
from .forms import AddRecipeForm


################
#### config ####
################

recipes_blueprint = Blueprint('recipes', __name__)


##########################
#### helper functions ####
##########################

def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ), 'info')


def get_all_recipes_with_users():
    # SQL: SELECT * FROM recipes JOIN users ON recipes.user_id = users.id;
    return db.session.query(Recipe, User).join(User).all()


################
#### routes ####
################

@recipes_blueprint.route('/')
def public_recipes():
    all_public_recipes = Recipe.query.filter_by(is_public=True)
    return render_template('public_recipes.html', public_recipes=all_public_recipes)


@recipes_blueprint.route('/recipes')
@login_required
def user_recipes():
    all_user_recipes = Recipe.query.filter_by(user_id=current_user.id)
    return render_template('user_recipes.html', user_recipes=all_user_recipes)


@recipes_blueprint.route('/add', methods=['GET', 'POST'])
@login_required
def add_recipe():
    form = AddRecipeForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            new_recipe = Recipe(form.recipe_title.data, form.recipe_description.data, current_user.id, True)
            db.session.add(new_recipe)
            db.session.commit()
            flash('New recipe, {}, added!'.format(new_recipe.recipe_title), 'success')
            return redirect(url_for('recipes.user_recipes'))
        else:
            flash_errors(form)
            flash('ERROR! Recipe was not added.', 'error')

    return render_template('add_recipe.html', form=form)


@recipes_blueprint.route('/recipe/<recipe_id>')
def recipe_details(recipe_id):
    recipe_with_user = db.session.query(Recipe, User).join(User).filter(Recipe.id == recipe_id).first()
    if recipe_with_user is not None:
        if recipe_with_user.Recipe.is_public:
            return render_template('recipe_detail.html', recipe=recipe_with_user)
        else:
            if current_user.is_authenticated and recipe_with_user.Recipe.user_id == current_user.id:
                return render_template('recipe_detail.html', recipe=recipe_with_user)
            else:
                flash('Error! Incorrect permissions to access this recipe.', 'error')
    else:
        flash('Error! Recipe does not exist.', 'error')
    return redirect(url_for('recipes.public_recipes'))
