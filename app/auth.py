from flask import Blueprint, request, jsonify, make_response, current_app, g
from app.models import User, db
from app.extensions import bcrypt
import jwt
import datetime
from app.utils import login_required

auth_bp = Blueprint('auth', __name__)

def generate_token(user_id):
    payload = {
        'user_id': user_id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1)
    }
    return jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256')

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'error': 'Email and password required', 'code': 'MISSING_FIELDS'}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({'error': 'Email already exists', 'code': 'EMAIL_EXISTS'}), 400

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    new_user = User(email=email, password_hash=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    token = generate_token(new_user.id)
    response = make_response(jsonify({'success': True}))
    response.set_cookie('auth_token', token, httponly=True, secure=True, samesite='None') # Set secure=True in prod
    return response, 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()

    if user and bcrypt.check_password_hash(user.password_hash, password):
        token = generate_token(user.id)
        response = make_response(jsonify({'success': True}))
        response.set_cookie('auth_token', token, httponly=True, secure=True, samesite='None')
        return response
    
    return jsonify({'error': 'Invalid credentials', 'code': 'INVALID_CREDENTIALS'}), 401

@auth_bp.route('/logout', methods=['POST'])
def logout():
    response = make_response(jsonify({'success': True}))
    response.set_cookie('auth_token', '', expires=0, httponly=True, secure=True, samesite='None')
    return response

@auth_bp.route('/me', methods=['GET'])
@login_required
def get_me():
    user = User.query.get(g.user_id)
    if not user:
        return jsonify({'error': 'User not found', 'code': 'USER_NOT_FOUND'}), 404
    return jsonify(user.to_dict())
