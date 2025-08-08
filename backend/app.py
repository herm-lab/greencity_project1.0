from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os
import re

app = Flask(__name__)
CORS(app)

# Настройка базы данных
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'users.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# Модель пользователя
class User(db.Model):
    __tablename__ = 'users'
    code = db.Column(db.String(6), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    class_info = db.Column(db.String(50), nullable=False)
    lids = db.Column(db.Integer, default=0)
    plastic = db.Column(db.Integer, default=0)
    batteries = db.Column(db.Integer, default=0)


POINTS_SYSTEM = {
    'lids': 5,
    'plastic': 3,
    'batteries': 10
}

# Создаём базу при первом запуске
with app.app_context():
    db.create_all()
    # Добавляем тестового пользователя если база пуста
    if not User.query.first():
        test_user = User(
            code='A12345',
            name='Иван Иванов',
            class_info='8А',
            lids=5,
            plastic=3,
            batteries=2
        )
        db.session.add(test_user)
        db.session.commit()


@app.route('/api/check-user', methods=['POST'])
def check_user():
    data = request.get_json()
    if not data or 'code' not in data:
        return jsonify({'error': 'Требуется код пользователя'}), 400

    code = data['code'].upper()
    if not re.match(r'^[A-Z]\d{5}$', code):
        return jsonify({'error': 'Неверный формат кода (A12345)'}), 400

    user_exists = db.session.query(db.exists().where(User.code == code)).scalar()
    return jsonify({'exists': user_exists})


@app.route('/api/user-stats/<code>', methods=['GET'])
def user_stats(code):
    user = User.query.get(code.upper())
    if not user:
        return jsonify({'error': 'Пользователь не найден'}), 404

    return jsonify({
        'name': user.name,
        'classInfo': user.class_info,
        'waste': {
            'lids': user.lids,
            'plastic': user.plastic,
            'batteries': user.batteries
        },
        'total_points': (
                user.lids * POINTS_SYSTEM['lids'] +
                user.plastic * POINTS_SYSTEM['plastic'] +
                user.batteries * POINTS_SYSTEM['batteries']
        )
    })


@app.route('/api/add-waste', methods=['POST'])
def add_waste():
    data = request.get_json()
    if not all(k in data for k in ['userCode', 'type', 'amount']):
        return jsonify({'error': 'Не хватает данных'}), 400

    waste_type = data['type']
    if waste_type not in POINTS_SYSTEM:
        return jsonify({'error': 'Неверный тип вторсырья'}), 400

    user = User.query.get(data['userCode'].upper())
    if not user:
        return jsonify({'error': 'Пользователь не найден'}), 404

    # Обновляем данные
    if waste_type == 'lids':
        user.lids += int(data['amount'])
    elif waste_type == 'plastic':
        user.plastic += int(data['amount'])
    elif waste_type == 'batteries':
        user.batteries += int(data['amount'])

    db.session.commit()

    return jsonify({
        'success': True,
        'newCount': getattr(user, waste_type)
    })


@app.route('/api/create-user', methods=['POST'])
def create_user():
    data = request.get_json()
    if not all(k in data for k in ['name', 'classInfo']):
        return jsonify({'error': 'Не хватает данных'}), 400

    # Генерация кода (первая буква + 5 цифр)
    first_letter = data['name'][0].upper()
    numbers = ''.join([str(i % 10) for i in range(1, 6)])
    code = f"{first_letter}{numbers}"

    if User.query.get(code):
        return jsonify({'error': 'Пользователь уже существует'}), 400

    new_user = User(
        code=code,
        name=data['name'],
        class_info=data['classInfo'],
        lids=0,
        plastic=0,
        batteries=0
    )
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'code': code}), 201


if __name__ == '__main__':
    app.run(debug=True, port=5000)