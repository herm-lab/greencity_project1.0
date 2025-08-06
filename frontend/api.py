import requests
from requests.exceptions import RequestException

BASE_URL = "http://localhost:5000/api"

def check_user(code):
    #Проверка на сущ. пользователя
    try:
        response = requests.post(
            f"{BASE_URL}/check-user",
            json={'code': code},
            timeout=5
        )
        return response.json().get('exists', False)
    except RequestException:
        return False

def get_user_stats(code):
    try:
        response = requests.get(
            f"{BASE_URL}/user-stats/{code}",
            timeout=5
        )
        return response.json()
    except RequestException as e:
        return {'error': str(e)}

def add_waste(user_code, waste_type, amount):
    try:
        response = requests.post(
            f"{BASE_URL}/add-waste",
            json={
                'userCode': user_code,
                'type': waste_type,
                'amount': amount
            },
            timeout=5
        )
        return response.json()
    except RequestException as e:
        return {'error': str(e)}

def create_user(name, class_info):
    try:
        response = requests.post(
            f"{BASE_URL}/create-user",
            json={
                'name': name,
                'classInfo': class_info
            },
            timeout=5
        )
        return response.json()
    except RequestException as e:
        return {'error': str(e)}