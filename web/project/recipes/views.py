# project/recipes/views.py

#################
#### imports ####
#################

from flask import render_template, Blueprint, request, redirect, url_for, flash, abort, jsonify
from flask_login import current_user, login_required
from project import db, images
from project.models import Recipe, User
from .forms import AddRecipeForm, EditRecipeForm
from random import random
import json


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


def add_uri_to_recipe(recipe):
    new_recipe = recipe
    new_recipe.id = url_for('recipes.api_get_recipe', recipe_id=recipe.id, _external=True)
    return new_recipe


########################
#### error handlers ####
########################

@recipes_blueprint.errorhandler(404)
def api_error(e):
    response = jsonify({'status': 404, 'error': 'not found (API!)', 'message': 'invalid resource URI'})
    response.status_code = 404
    return response


@recipes_blueprint.errorhandler(405)
def api_error(e):
    response = jsonify({'status': 405, 'error': 'method not supported (API!)', 'message': 'method is not supported'})
    response.status_code = 405
    return response


@recipes_blueprint.errorhandler(500)
def api_error(e):
    response = jsonify({'status': 500, 'error': 'internal server error (API!)', 'message': 'internal server error occurred'})
    response.status_code = 500
    return response


################
#### routes ####
################

@recipes_blueprint.route('/')
def public_recipes():
    all_public_recipes = Recipe.query.filter(Recipe.is_public == True, Recipe.image_url != None).order_by(Recipe.rating.desc()).limit(4)
    return render_template('public_recipes.html', public_recipes=all_public_recipes)


@recipes_blueprint.route('/recipes/<recipe_type>')
@login_required
def user_recipes(recipe_type='All'):
    if recipe_type in ['Breakfast', 'Lunch', 'Dinner', 'Dessert', 'Side_Dish']:
        my_recipes = Recipe.query.filter_by(user_id=current_user.id, recipe_type=recipe_type)
        return render_template('user_recipes.html', user_recipes=my_recipes, recipe_type=recipe_type)
    elif recipe_type == 'All':
        my_recipes = Recipe.query.filter_by(user_id=current_user.id)
        return render_template('user_recipes.html', user_recipes=my_recipes, recipe_type=recipe_type)
    else:
        flash('ERROR! Invalid recipe type selected.', 'error')

    return redirect(url_for('recipes.public_recipes'))


@recipes_blueprint.route('/add', methods=['GET', 'POST'])
@login_required
def add_recipe():
    # Cannot pass in 'request.form' to AddRecipeForm constructor, as this will cause 'request.files' to not be
    # sent to the form.  This will cause AddRecipeForm to not see the file data.
    # Flask-WTF handles passing form data to the form, so not parameters need to be included.
    form = AddRecipeForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            filename = images.save(request.files['recipe_image'])
            url = images.url(filename)
            new_recipe = Recipe(form.recipe_title.data,
                                form.recipe_description.data,
                                current_user.id,
                                form.recipe_public.data,
                                filename,
                                url,
                                form.recipe_type.data,
                                form.recipe_rating.data,#  or None,
                                form.recipe_ingredients.data,
                                form.recipe_steps.data,
                                form.recipe_inspiration.data)
            db.session.add(new_recipe)
            db.session.commit()
            flash('New recipe, {}, added!'.format(new_recipe.recipe_title), 'success')
            return redirect(url_for('recipes.user_recipes', recipe_type='All'))
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


@recipes_blueprint.route('/delete/<recipe_id>')
@login_required
def delete_recipe(recipe_id):
    recipe = Recipe.query.filter_by(id=recipe_id).first()
    if recipe is not None:
        if recipe.user_id == current_user.id:
            db.session.delete(recipe)
            db.session.commit()
            flash('{} was deleted.'.format(recipe.recipe_title), 'success')
            return redirect(url_for('recipes.user_recipes', recipe_type='All'))
        else:
            flash('Error! Incorrect permissions to delete this recipe.', 'error')
    else:
        flash('Error! Recipe does not exist.', 'error')
    return redirect(url_for('recipes.public_recipes'))


@recipes_blueprint.route('/edit/<recipe_id>', methods=['GET', 'POST'])
@login_required
def edit_recipe(recipe_id):
    # Cannot pass in 'request.form' to AddRecipeForm constructor, as this will cause 'request.files' to not be
    # sent to the form.  This will cause AddRecipeForm to not see the file data.
    # Flask-WTF handles passing form data to the form, so not parameters need to be included.
    form = EditRecipeForm()
    recipe = Recipe.query.filter_by(id=recipe_id).first()

    if request.method == 'POST':
        if form.validate_on_submit():
            update_counter = 0

            if form.recipe_title.data is not None and form.recipe_title.data != recipe.recipe_title:
                flash('DEBUG: Updating recipe.recipe_title to {}.'.format(form.recipe_title.data), 'debug')
                update_counter += 1
                recipe.recipe_title = form.recipe_title.data

            if form.recipe_description.data is not None and form.recipe_description.data != recipe.recipe_description:
                flash('DEBUG: Updating recipe.recipe_description to {}.'.format(form.recipe_description.data), 'debug')
                update_counter += 1
                recipe.recipe_description = form.recipe_description.data

            if form.recipe_public.data != recipe.is_public:
                flash('DEBUG: Updating recipe.is_public to {}.'.format(form.recipe_public.data), 'debug')
                update_counter += 1
                recipe.is_public = form.recipe_public.data

            if form.recipe_type.data != recipe.recipe_type:
                flash('DEBUG: Updating recipe.recipe_type to {}.'.format(form.recipe_type.data), 'debug')
                update_counter += 1
                recipe.recipe_type = form.recipe_type.data

            if form.recipe_rating.data != str(recipe.rating):
                flash('DEBUG: Updating recipe.rating from {} to {}.'.format(str(recipe.rating), form.recipe_rating.data), 'debug')
                update_counter += 1
                recipe.rating = form.recipe_rating.data

            if form.recipe_image.has_file():
                flash('DEBUG: Updating recipe.image_filename to {}.'.format(form.recipe_image.data), 'debug')
                update_counter += 1
                filename = images.save(request.files['recipe_image'])
                recipe.image_filename = filename
                recipe.image_url = images.url(filename)

            if form.recipe_ingredients.data != recipe.ingredients:
                flash('DEBUG: Updating recipe.ingredients to {}.'.format(form.recipe_ingredients.data), 'debug')
                update_counter += 1
                recipe.ingredients = form.recipe_ingredients.data

            if form.recipe_steps.data != recipe.recipe_steps:
                flash('DEBUG: Updating recipe.recipe_steps to {}.'.format(form.recipe_steps.data), 'debug')
                update_counter += 1
                recipe.recipe_steps = form.recipe_steps.data

            if form.recipe_inspiration.data is not None and form.recipe_inspiration.data != recipe.inspiration:
                flash('DEBUG: Updating recipe.inspiration to {}.'.format(form.recipe_inspiration.data), 'debug')
                update_counter += 1
                recipe.inspiration = form.recipe_inspiration.data

            if update_counter > 0:
                db.session.add(recipe)
                db.session.commit()
                flash('Recipe has been updated for {}.'.format(recipe.recipe_title), 'success')
            else:
                flash('No updates made to the recipe ({}). Please update at least one field.'.format(recipe.recipe_title), 'error')

            return redirect(url_for('recipes.recipe_details', recipe_id=recipe_id))
        else:
            flash_errors(form)
            flash('ERROR! Recipe was not edited.', 'error')

    return render_template('edit_recipe.html', form=form, recipe=recipe)


@recipes_blueprint.route('/whats_for_dinner')
@login_required
def whats_for_dinner():
    dinner_recipe_found = True
    dinner_takeout_recommendation = False
    dinner_recipe = None
    dinner_recipes = Recipe.query.filter_by(recipe_type='Dinner').all()

    if len(dinner_recipes) > 0:
        proposed_index = int((random() * 1000) % len(dinner_recipes))

        if len(dinner_recipes) < 8:
            dinner_recipe = dinner_recipes[proposed_index]
        else:
            if proposed_index % 8 == 0:
                dinner_takeout_recommendation = True
            else:
                dinner_recipe = dinner_recipes[proposed_index]
    else:
        dinner_recipe_found = False

    return render_template('whats_for_dinner.html',
                           recipe_found=dinner_recipe_found,
                           takeout_recommendation=dinner_takeout_recommendation,
                           recipe=dinner_recipe)


###################
####  API v1.1 ####
###################

@recipes_blueprint.route('/api/v1_1/recipes', methods=['GET'])
def api_get_all_recipes():
    recipes = Recipe.query.all()
    # recipes = Recipe.query.filter_by(user_id=1).all()
    # recipes = Recipe.query.filter_by(user_id=4).all()

    if len(recipes) == 0:
        return jsonify({'Error': 'No recipes were found.'})

    json_output = []
    for recipe in recipes:
        recipe_json = {'id': url_for('recipes.api_get_recipe', recipe_id=recipe.id, _external=True),
                       'recipe': recipe.recipe_title,
                       'description': recipe.recipe_description,
                       'public': recipe.is_public,
                       'image_filename': recipe.image_filename,
                       'image_url': recipe.image_url}
        json_output.append(recipe_json)

    return jsonify(json_output)


@recipes_blueprint.route('/api/v1_1/recipes/<int:recipe_id>', methods=['GET'])
def api_get_recipe(recipe_id):
    recipe = Recipe.query.filter_by(id=recipe_id).first()
    if recipe is not None:
        return jsonify({'recipe': recipe.recipe_title,
                        'description': recipe.recipe_description,
                        'public': recipe.is_public,
                        'image_filename': recipe.image_filename,
                        'image_url': recipe.image_url})
    else:
        abort(404)


@recipes_blueprint.route('/api/v1_1/recipes', methods=['POST'])
def api_create_recipe():
    if not request.json or 'title' not in request.json:
        abort(404)

    user = User.query.filter_by(email='patkennedy79@gmail.com').first()
    new_recipe = Recipe(request.json['title'],
                        request.json['description'],
                        user.id,
                        True,
                        recipe_type=request.json['recipe_type'])
    db.session.add(new_recipe)
    db.session.commit()

    return jsonify({'recipe': new_recipe.recipe_title,
                    'description': new_recipe.recipe_description,
                    'public': new_recipe.is_public,
                    'filename': new_recipe.image_filename}), 201


@recipes_blueprint.route('/api/v1_1/recipes/<int:recipe_id>', methods=['DELETE'])
def api_delete_recipe(recipe_id):
    recipe = Recipe.query.filter_by(id=recipe_id).first()
    if recipe is not None:
        db.session.delete(recipe)
        db.session.commit()
        return jsonify({'result': True})
    else:
        abort(404)


@recipes_blueprint.route('/api/v1_1/recipes/<int:recipe_id>', methods=['PUT'])
def api_update_recipe(recipe_id):
    recipe = Recipe.query.filter_by(id=recipe_id).first()
    if recipe is not None:
        if 'recipe_image' in request.files:
            print('request.files: {}'.format(str(request.files)))
            print('request.files[recipe_image]: {}'.format(str(request.files['recipe_image'])))
            print('request.files[recipe_image].filename: {}'.format(str(request.files['recipe_image'].filename)))
            filename = images.save(request.files['recipe_image'])
            url = images.url(filename)

            recipe.image_filename = filename
            recipe.image_url = images.url(filename)
            print('filename: {}'.format(filename))
            print('url: {}'.format(url))
            db.session.add(recipe)
            db.session.commit()

            return jsonify({'filename': filename,
                            'url': url})
        else:
            update_counter = 0
            if 'title' in request.json:
                print('Updating title...')
                update_counter += 1
                recipe.recipe_title = request.json.get('title')
            if 'description' in request.json:
                print('Updating description...')
                update_counter += 1
                recipe.recipe_description = request.json.get('description')
            if 'recipe_type' in request.json:
                print('Updating recipe_type...')
                update_counter += 1
                recipe.recipe_type = request.json.get('recipe_type')

            if update_counter > 0:
                db.session.add(recipe)
                db.session.commit()
                return jsonify({'result': True})
            else:
                return jsonify({'result': False})
    else:
        return jsonify({'Error': 'recipe not found in database.'})


###################
####  API v1.2 ####
###################

@recipes_blueprint.route('/api/v1_2/recipes', methods=['GET'])
def api1_2_get_all_recipes():
    return jsonify({'recipes': [recipe.get_url() for recipe in Recipe.query.all()]})


@recipes_blueprint.route('/api/v1_2/recipes/<int:recipe_id>', methods=['GET'])
def api1_2_get_recipe(recipe_id):
    return jsonify(Recipe.query.get_or_404(recipe_id).export_data())


@recipes_blueprint.route('/api/v1_2/recipes', methods=['POST'])
def api1_2_create_recipe():
    new_recipe = Recipe()
    new_recipe.import_data(request.json)
    db.session.add(new_recipe)
    db.session.commit()
    return jsonify({}), 201, {'Location': new_recipe.get_url()}


@recipes_blueprint.route('/api/v1_2/recipes/<int:recipe_id>', methods=['PUT'])
def api1_2_update_recipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    recipe.import_data(request.json)
    db.session.add(recipe)
    db.session.commit()
    return jsonify({'result': True})


@recipes_blueprint.route('/api/v1_2/recipes/<int:recipe_id>', methods=['DELETE'])
def api1_2_delete_recipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    db.session.delete(recipe)
    db.session.commit()
    return jsonify({'result': True})
