from project import db
from project.models import Recipe, User


# drop all of the existing database tables
db.drop_all()

# create the database and the database table
db.create_all()

# insert recipe data
recipe1 = Recipe('Slow-Cooker Tacos', 'Delicious ground beef that has been simmering in taco seasoning and sauce.  Perfect with hard-shelled tortillas!')
recipe2 = Recipe('Hamburgers', 'Classic dish elevated with pretzel buns.')
recipe3 = Recipe('Mediterranean Chicken', 'Grilled chicken served with pitas, hummus, and sauted vegetables.')
db.session.add(recipe1)
db.session.add(recipe2)
db.session.add(recipe3)

# commit the changes for the recipes
db.session.commit()

# insert user data
user1 = User('patkennedy79@yahoo.com', 'password1234')
user2 = User('kennedyfamilyrecipes@gmail.com', 'PaSsWoRd')
user3 = User('blaa@blaa.com', 'MyFavPassword')
db.session.add(user1)
db.session.add(user2)
db.session.add(user3)

# commit the changes for the recipes
db.session.commit()

user1.is_correct_password('password1234')