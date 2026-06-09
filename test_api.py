import requests
res = requests.post('http://localhost:8000/users/', json={'name':'Test', 'surname':'Test', 'email':'test2@test.com', 'password':'Pass123()', 'phone':'', 'gender':'', 'birth_date':''})
print(res.status_code)
print(res.text)
