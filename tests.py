import requests

BASE = "http://127.0.0.1:5000/"
response = requests.post(BASE + "login", {"email" : "gmanager@hospital.com","password": "gmpass"})
print(response.json())
