import requests
import json


# APi v1.0
# url = 'http://192.168.99.100/api/v1_0/add_recipe'
# payload = {'title': 'Hamburgers', 'description': 'Delicious hamburgers served with sourdough bread', 'recipe_type': 'Dinner'}
#
# r = requests.post(url, json=payload)
# print(r.text)


# API v1.1
# url = 'http://192.168.99.100/api/v1_2/recipes'
url = 'http://localhost:5000/api/v1_2/recipes'
payload = {'title': 'BBQ Chicken', 'description': 'Taste treat', 'recipe_type': 'Dinner'}
# file = {'file': ('IMG_6127.JPG', open('IMG_6127.JPG', 'rb'), 'multipart/form-data', {'Expires': '0'})}
# file = {'IMG_6127.JPG': open('IMG_6127.JPG', 'rb')}
_file = 'IMG_6127.JPG'
json_data = {'title': 'BBQ Chicken', 'description': 'Taste treat', 'recipe_type': 'Dinner'}

# with open(_file, 'rb') as recipe_image:
#     try:
#         response = requests.post(url=url, data=payload, files={recipe_image: 'IMG_6127.JPG'}, verify=False)
#     except TimeoutError:
#         print("The connection timed out!")
#     else:
#         print(response)
#         print(response.text)

# r = requests.post(url, files={'recipe_image': open('IMG_6127.JPG', 'rb')})
r = requests.post(url, files={'recipe_image': open('IMG_6127.JPG', 'rb'), 'title': 'BBQ Chicken'})
print(r.status_code)
print(r.text)

        # r = requests.post(url, json=payload, files=file)
# print(r.text)


# def upload_file(local_file, remote_file):
#     params = {"file": os.path.basename(remote_file),
#               "folder": os.path.dirname(remote_file),
#               "submit": "Submit"}
#     with open(local_file, 'rb') as file_:
#         try:
#            response = requests.post(url=URL, data=params, auth=(USER, PASSWORD),
#                                     files={"zip_file": file_}, verify=False)
#         except TimeoutError:
#             print("Connection timed out!")
#         else:
#             print(response)