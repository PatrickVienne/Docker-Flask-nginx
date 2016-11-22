import requests


# URL_BASE = 'http://192.168.99.100/'
URL_BASE = 'http://localhost:5000/'


# API v1.1 - GET (All)
print('Retrieving all recipes...')
url = URL_BASE + 'api/v1_1/recipes'
r = requests.get(url)
print(r.text)

# API v1.1 - GET (Individual Recipe)
print('Retrieving recipe #2...')
url = URL_BASE + 'api/v1_1/recipes/2'
r = requests.get(url)
print(r.text)

# API v1.1 - DELETE
print('Deleting recipe #1...')
url = URL_BASE + 'api/v1_1/recipes/1'
r = requests.delete(url)
print(r.text)

# API v1.1 - GET (All)
print('Retrieving all recipes...')
url = URL_BASE + 'api/v1_1/recipes'
r = requests.get(url)
print(r.text)

# API v1.0 - POST
print('Add a new recipe...')
url = URL_BASE + 'api/v1_0/recipes'
json_data = {'title': 'Tacos2', 'description': 'My favorite tacos!', 'recipe_type': 'Dinner'}
r = requests.post(url, json=json_data)
print(r.status_code)
print(r.text)

# API v1.1 - PUT
print('Updating recipe #2...')
url = URL_BASE + 'api/v1_1/recipes/2'
json_data = {'description': 'My favorite recipe'}
r = requests.put(url, json=json_data)
print(r.text)

# API v1.1 - GET (All)
print('Retrieving all recipes...')
url = URL_BASE + 'api/v1_1/recipes'
r = requests.get(url)
print(r.status_code)
print(r.headers)
print(r.text)
