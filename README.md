[![build status](https://gitlab.com/patkennedy79/flask_recipe_app/badges/master/build.svg)](https://gitlab.com/patkennedy79/flask_recipe_app/commits/master)
[![say thanks](https://img.shields.io/badge/Say%20Thanks-!-1EAEDB.svg)](https://saythanks.io/to/patkennedy79)
## Synopsis

Family Recipe web application for keeping track of your favorite recipes.

## Website
http://www.kennedyfamilyrecipes.com

## What Does This Tool Do?
Keeps track of all your recipes.

## How to Run

In the top-level folder, run the development server:
    % python run.py

Go to your favorite web browser and open:
    http://locallhost:5000

## Key Python Modules Used

- Flask - web framework
- Jinga2 - templating engine
- SQLAlchemy - ORM (Object Relational Mapper)
- Flask-Bcrypt - password hashing
- Flask-Login - support for user management
- Flask-Migrate - database migrations
- Flask-WTF - simplifies forms
- itsdangerous - helps with user management, especially tokens

This application is written using Python 3.4.3.  The database used is PostgreSQL.

## Unit Testing

In the top-level folder:
    % nose2

For running a specific module:
    % nose2 -v project.tests.test_recipes_api