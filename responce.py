import requests

url = 'http://localhost:8080/api/partners/2/cashback'
data = {
    "cashback" : 100
}
response = requests.put(url, json=data)# Замените на ваш адрес сервера Flask


