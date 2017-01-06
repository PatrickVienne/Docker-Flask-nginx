import requests


# URL_BASE = 'http://192.168.99.100/'
URL_BASE = 'http://localhost:5000/'
auth=('patkennedy79@gmail.com', 'knugelwerken')

# API v1.2 - GET (All)
print('Retrieving all recipes...')
url = URL_BASE + 'api/v1_2/recipes'
r = requests.get(url, auth=auth)
print(r.status_code)
print(r.text)

# API v1.2 - GET (Individual Recipe)
print('Retrieving recipe #2...')
url = URL_BASE + 'api/v1_2/recipes/2'
r = requests.get(url, auth=auth)
print(r.status_code)
print(r.text)

# API v1.2 - POST
print('Add a new recipe...')
url = URL_BASE + 'api/v1_2/recipes'
json_data = {'title': 'Tacos2', 'description': 'My favorite tacos!', 'recipe_type': 'Dinner'}
r = requests.post(url, json=json_data, auth=auth)
print(r.status_code)
print(r.headers)
print(r.text)

# API v1.2 - GET (All)
print('Retrieving all recipes...')
url = URL_BASE + 'api/v1_2/recipes'
r = requests.get(url, auth=auth)
print(r.status_code)
print(r.text)

# API v1.2 - PUT
print('Updating recipe #2...')
url = URL_BASE + 'api/v1_2/recipes/2'
json_data = {'title': 'Updated recipe', 'description': 'My favorite recipe'}
r = requests.put(url, json=json_data, auth=auth)
print(r.status_code)
print(r.headers)
print(r.text)

# API v1.2 - DELETE
print('Deleting recipe #1...')
url = URL_BASE + 'api/v1_2/recipes/1'
r = requests.delete(url, auth=auth)
print(r.status_code)
print(r.text)

# API v1.2 - GET (All)
print('Retrieving all recipes...')
url = URL_BASE + 'api/v1_2/recipes'
r = requests.get(url, auth=auth)
print(r.status_code)
print(r.text)

# API v1.2 - GET (Individual Recipe - INVALID)
print('Retrieving recipe #2...')
url = URL_BASE + 'api/v1_2/recipes/'
r = requests.get(url, auth=auth)
print(r.status_code)
print(r.text)

# API v1.2 - GET (Individual Recipe - INVALID)
print('Retrieving recipe #17...')
url = URL_BASE + 'api/v1_2/recipes/17'
r = requests.get(url, auth=auth)
print(r.status_code)
print(r.text)


# # API v1.1 - GET (All)
# print('Retrieving all recipes...')
# url = URL_BASE + 'api/v1_1/recipes'
# r = requests.get(url)
# print(r.text)
#
# # API v1.1 - GET (Individual Recipe)
# print('Retrieving recipe #2...')
# url = URL_BASE + 'api/v1_1/recipes/2'
# r = requests.get(url)
# print(r.text)
#
# # API v1.1 - DELETE
# print('Deleting recipe #1...')
# url = URL_BASE + 'api/v1_1/recipes/1'
# r = requests.delete(url)
# print(r.text)
#
# # API v1.1 - GET (All)
# print('Retrieving all recipes...')
# url = URL_BASE + 'api/v1_1/recipes'
# r = requests.get(url)
# print(r.text)
#
# # API v1.1 - POST
# print('Add a new recipe...')
# url = URL_BASE + 'api/v1_1/recipes'
# json_data = {'title': 'Tacos2', 'description': 'My favorite tacos!', 'recipe_type': 'Dinner'}
# r = requests.post(url, json=json_data)
# print(r.status_code)
# print(r.text)
#
# # API v1.1 - PUT
# print('Updating recipe #2...')
# url = URL_BASE + 'api/v1_1/recipes/2'
# json_data = {'description': 'My favorite recipe'}
# r = requests.put(url, json=json_data)
# print(r.status_code)
# print(r.headers)
# print(r.text)
#
# # API v1.1 - GET (All)
# print('Retrieving all recipes...')
# url = URL_BASE + 'api/v1_1/recipes'
# r = requests.get(url)
# print(r.status_code)
# print(r.headers)
# print(r.text)
#
# # API v1.1 - PUT (Add image)
# print('Updating recipe #2 with recipe image...')
# url = URL_BASE + 'api/v1_1/recipes/2'
# r = requests.put(url, files={'recipe_image': open('IMG_6127.JPG', 'rb')})
# print(r.status_code)
# print(r.headers)
# print(r.text)
#
# # API v1.1 - GET (All)
# print('Retrieving all recipes...')
# url = URL_BASE + 'api/v1_1/recipes'
# r = requests.get(url)
# print(r.text)
