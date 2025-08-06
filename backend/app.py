from flask import Flask, jsonify, request
from flask_cors import CORS
import os
import json
import re
from werkzeug.exceptions import HTTPException

app = Flask(__name__)
CORS(app)

DB_FILE = 'database.txt'
POINTS_SYSTEM = {
    'lids': 5,
    'plastic': 3,
    'batteries': 10
}


def init_db():
    if not os.path.exists(DB_FILE):
        with open(DB_FILE, 'w') as f:
            json.dump({
                "A12345": {
                    "name": "Иван Иванов",
                    "class": "8А",
                    "waste": {
                        "lids": 0,
                        "plastic": 0,
                        "batteries": 0
                    }
                }
            }, f, indent=2)
#возможно indent=4

def read_db():
    #Проверка format
    try:
        with open(DB_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            if not isinstance(data, dict):
                raise ValueError("Invalid database format")
            return data
    except (FileNotFoundError, json.JSONDecodeError, ValueError) as e:
        print(f"Database read error: {str(e)}")
        init_db()
        return read_db()



def write_db(data):
    #Запись с проверкой format
    if not isinstance(data, dict):
        raise ValueError("Data must be a dictionary")

    with open(DB_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
#возможно indent=4

def validate_code(code):
    #паттеринг
    return re.match(r'^[A-Z]\d{5}$', code) is not None


@app.route('/api/check-user', methods=['POST'])
def check_user():
    try:
        data = request.get_json()
        if not data or 'code' not in data:
            return jsonify({'error': 'Missing code parameter'}), 400

        code = data['code'].upper()
        if not re.match(r'^[A-Z]\d{5}$', code):
            return jsonify({'error': 'Invalid code format (A12345)'}), 400

        db = read_db()
        return jsonify({'exists': code in db})

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/add-waste', methods=['POST'])
def add_waste():
    data = request.get_json()
    if not data or 'userCode' not in data or 'type' not in data or 'amount' not in data:
        return jsonify({'error': 'Не хватает данных'}), 400

    user_code = data['userCode'].upper()
    db = read_db()

    if user_code not in db:
        return jsonify({'error': 'Пользователь не найден'}), 404

    waste_type = data['type']
    if waste_type not in POINTS_SYSTEM:
        return jsonify({'error': 'Неверный тип вторсырья'}), 400

    db[user_code]['waste'][waste_type] += int(data['amount'])
    write_db(db)

    return jsonify({
        'success': True,
        'newCount': db[user_code]['waste'][waste_type]
    })


@app.route('/api/user-stats/<code>', methods=['GET'])
def user_stats(code):
    db = read_db()
    code = code.upper()

    if code not in db:
        return jsonify({'error': 'Пользователь не найден'}), 404

    user_data = db[code]
    return jsonify({
        'name': user_data['name'],
        'class': user_data['class'],
        'waste': user_data['waste'],
        'total_points': sum(
            user_data['waste'][k] * POINTS_SYSTEM.get(k, 0)
            for k in user_data['waste']
        )
    })


@app.route('/api/create-user', methods=['POST'])
def create_user():
    data = request.get_json()
    if not data or 'name' not in data or 'classInfo' not in data:
        return jsonify({'error': 'Недостаточно данных'}), 400

    first_letter = data['name'][0].upper()
    numbers = ''.join([str(i) for i in range(1, 6)])  # Пример: A12345
    code = f"{first_letter}{numbers}"

    db = read_db()
    if code in db:
        return jsonify({'error': 'Пользователь уже существует'}), 400

    db[code] = {
        'name': data['name'],
        'class': data['classInfo'],
        'waste': {
            'lids': 0,
            'plastic': 0,
            'batteries': 0
        }
    }
    write_db(db)

    return jsonify({'code': code}), 201


if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5000)