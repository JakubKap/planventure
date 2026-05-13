from flask import Blueprint, jsonify, request

from extensions import db
from jwt_utils import create_jwt_access_token, create_jwt_refresh_token
from models import User
from utils import is_valid_email

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['POST'])
def register():
    payload = request.get_json(silent=True) or {}
    email = (payload.get('email') or '').strip().lower()
    password = payload.get('password') or ''

    if not email or not password:
        return jsonify({
            'error': 'Email and password are required.',
            'fields': ['email', 'password']
        }), 400

    if not is_valid_email(email):
        return jsonify({'error': 'Please provide a valid email address.'}), 400

    if len(password) < 8:
        return jsonify({'error': 'Password must be at least 8 characters long.'}), 400

    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({'error': 'Email already registered.'}), 409

    user = User(email=email)
    user.set_password(password)

    db.session.add(user)
    db.session.commit()

    return jsonify({'user': user.to_dict()}), 201


@auth_bp.route('/login', methods=['POST'])
def login():
    payload = request.get_json(silent=True) or {}
    email = (payload.get('email') or '').strip().lower()
    password = payload.get('password') or ''

    if not email or not password:
        return jsonify({
            'error': 'Email and password are required.',
            'fields': ['email', 'password']
        }), 400

    if not is_valid_email(email):
        return jsonify({'error': 'Please provide a valid email address.'}), 400

    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(password):
        return jsonify({'error': 'Invalid email or password.'}), 401

    access_token = create_jwt_access_token(identity=str(user.id))
    refresh_token = create_jwt_refresh_token(identity=user.id)

    return jsonify({
        'access_token': access_token,
        'refresh_token': refresh_token,
        'token_type': 'Bearer',
        'user': user.to_dict()
    }), 200
