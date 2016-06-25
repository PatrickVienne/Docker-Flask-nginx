# project/recipes/views.py

#################
#### imports ####
#################

from flask import render_template, Blueprint


################
#### config ####
################

recipes_blueprint = Blueprint('recipes', __name__, template_folder='templates')


################
#### routes ####
################

@recipes_blueprint.route('/')
def index():
    return render_template('index.html')
