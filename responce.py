import requests

url = 'http://localhost:8080/api/partners/3/cashback'
data = {
    "cashback": 200,
    "date": "2024-05-24"
}
response = requests.put(url, json=data)# Замените на ваш адрес сервера Flask
if response.status_code == 200:
    print("Cashback updated successfully!")





