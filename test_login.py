import requests
res = requests.post('http://localhost:8000/auth/login', json={'email':'test2@test.com', 'password':'Pass123()'})
print(res.status_code)
print(res.text)
