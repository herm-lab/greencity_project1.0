import requests
from requests.exceptions import RequestException
import json

BASE_URL = "http://localhost:5000/api"

def check_user(code):
    """Проверяет существование пользователя"""
    try:
        response = requests.post(
            f"{BASE_URL}/check-user",
            json={'code': code},
            timeout=5
        )
        response.raise_for_status()
        return response.json().get('exists', False)
    except (RequestException, json.JSONDecodeError) as e:
        print(f"[API ERROR] check_user: {str(e)}")
        return False

def get_user_stats(code):
    """Получает статистику пользователя"""
    try:
        response = requests.get(
            f"{BASE_URL}/user-stats/{code}",
            timeout=5
        )
        response.raise_for_status()
        return response.json()
    except (RequestException, json.JSONDecodeError) as e:
        print(f"[API ERROR] get_user_stats: {str(e)}")
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
        response.raise_for_status()  # Проверка на ошибки HTTP
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"[API ERROR] Ошибка при добавлении: {str(e)}")
        return {'error': str(e)}

def create_user(name, class_info):
    """Создает нового пользователя"""
    try:
        response = requests.post(
            f"{BASE_URL}/add-user",
            json={
                'name': name,
                'classInfo': class_info
            },
            timeout=5
        )
        response.raise_for_status()
        return response.json()
    except (RequestException, json.JSONDecodeError) as e:
        print(f"[API ERROR] create_user: {str(e)}")
        return {'error': str(e)}