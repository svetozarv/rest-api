import json
import requests

url = "http://127.0.0.1:5000/products/"

header = {
    "Content-Type" : "application/json",
    "Accept" : "application/json",
}

data = {
    'name': 'requests', 
    'id': '100', 
    'description': 'test from requests',
    'version': '0'
}

response = requests.post(url, headers=header, data=json.dumps(data))
print(response)
print(response.headers)
print(response.content)
