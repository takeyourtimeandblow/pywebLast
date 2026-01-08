from flask import Blueprint, jsonify, request
from db_session import create_session
from models.user import User
from werkzeug.security import generate_password_hash


user_api = Blueprint(
    'user_api',
    __name__,
    template_folder='templates'
)

@user_api.route('/api/users', methods=['GET'])
def get_users():
    session = create_session()
    users = session.query(User).all()

    return jsonify({
        'users': [
            {
                'id': user.id,
                'surname': user.surname,
                'name': user.name,
                'age': user.age,
                'position': user.position,
                'speciality': user.speciality,
                'address': user.address,
                'city_from': user.city_from,
                'email': user.email
            } for user in users
        ]
    })

@user_api.route('/api/users/<int:user_id>', methods=['GET'])
def get_one_user(user_id):
    session = create_session()
    user = session.get(User, user_id)

    if not user:
        return jsonify({'error': 'Not found'}), 404

    return jsonify({
        'user': {
            'id': user.id,
            'surname': user.surname,
            'name': user.name,
            'age': user.age,
            'position': user.position,
            'speciality': user.speciality,
            'address': user.address,
            'city_from': user.city_from,
            'email': user.email
        }
    })

@user_api.route('/api/users', methods=['POST'])
def add_user():
    session = create_session()

    if not request.json:
        return jsonify({'error': 'Empty request'}), 400

    user = User(
        surname=request.json.get('surname'),
        name=request.json.get('name'),
        age=request.json.get('age'),
        position=request.json.get('position'),
        speciality=request.json.get('speciality'),
        address=request.json.get('address'),
        city_from=request.json.get('city_from'),
        email=request.json.get('email'),
        hashed_password=generate_password_hash(
            request.json.get('password', '')
        )
    )

    session.add(user)
    session.commit()

    return jsonify({'success': 'OK'})

@user_api.route('/api/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    session = create_session()
    user = session.get(User, user_id)

    if not user:
        return jsonify({'error': 'Not found'}), 404

    session.delete(user)
    session.commit()

    return jsonify({'success': 'OK'})

@user_api.route('/api/users/<int:user_id>', methods=['PUT'])
def edit_user(user_id):
    session = create_session()
    user = session.get(User, user_id)

    if not user:
        return jsonify({'error': 'Not found'}), 404

    if not request.json:
        return jsonify({'error': 'Empty request'}), 400

    user.surname = request.json.get('surname', user.surname)
    user.name = request.json.get('name', user.name)
    user.age = request.json.get('age', user.age)
    user.position = request.json.get('position', user.position)
    user.speciality = request.json.get('speciality', user.speciality)
    user.address = request.json.get('address', user.address)
    user.email = request.json.get('email', user.email)

    session.commit()

    return jsonify({'success': 'OK'})
