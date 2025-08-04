from flask import Flask, jsonify, request
from flask_cors import CORS
import os
import json
import random
import string
from werkzeug.exceptions import HTTPException
POINTS_SYSTEM = {
    'lids': 5,
    'plastic': 3,
    'batteries': 10
}

app = Flask(__name__)
CORS(app)

DB_FILE = 'database.txt'


def init_db():
    """Инициализирует базу данных если её нет"""
    if not os.path.exists(DB_FILE):
        with open(DB_FILE, 'w') as f:
            json.dump({}, f)


def read_db():
    """Читает базу данных с обработкой ошибок"""
    try:
        with open(DB_FILE, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def write_db(data):
    """Записывает данные в файл"""
    with open(DB_FILE, 'w') as f:
        json.dump(data, f, indent=2)


@app.route('/api/check-user', methods=['POST'])
def check_user():
    try:
        data = request.get_json()
        if not data or 'code' not in data:
            return jsonify({'error': 'Missing code parameter'}), 400

        db = read_db()
        return jsonify({
            'exists': data['code'] in db,
            'debug': list(db.keys())  # Для отладки
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/add-waste', methods=['POST'])
def add_waste():
    try:
        # Получаем JSON-данные
        data = request.get_json()

        # Проверяем обязательные поля
        if not data or 'userCode' not in data or 'type' not in data or 'amount' not in data:
            return jsonify({'error': 'Не хватает данных'}), 400

        # Читаем базу данных
        db = read_db()
        user_code = data['userCode']

        # Проверяем существование пользователя
        if user_code not in db:
            return jsonify({'error': 'Пользователь не найден'}), 404

        # Проверяем тип мусора
        valid_types = ['lids', 'plastic', 'batteries']
        if data['type'] not in valid_types:
            return jsonify({'error': 'Неверный тип мусора'}), 400

        # Обновляем данные
        db[user_code]['waste'][data['type']] += int(data['amount'])
        write_db(db)

        # Возвращаем успешный ответ
        return jsonify({
            'success': True,
            'newCount': db[user_code]['waste'][data['type']]
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/user-stats/<code>', methods=['GET'])
def user_stats(code):
    """Возвращает статистику пользователя"""
    try:
        db = read_db()
        if code not in db:
            return jsonify({'error': 'User not found'}), 404

        return jsonify({
            'name': db[code]['name'],
            'class': db[code]['class'],
            'waste': db[code]['waste'],
            'total_points': sum(
                db[code]['waste'][k] * POINTS_SYSTEM.get(k, 0)
                for k in db[code]['waste']
            )
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.errorhandler(500)
def handle_500(e):
    return jsonify({'error': 'Internal server error'}), 500


if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5000)
