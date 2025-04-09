from flask import jsonify
from app import db
from app.models import User, APIKey
from app.utils.security import hash_password
from flask_login import login_user, current_user 
import secrets
import bcrypt
import re

def register_user(data):
    email = data.get('email', '').strip()
    password = data.get('password', '').strip()

    if not email or not password:
        return jsonify({'error': 'Both email and password are required.'}), 400

    email_regex = r'^\S+@\S+\.\S+$'
    if not re.match(email_regex, email):
        return jsonify({'error': 'Invalid email format.'}), 400

    if len(password) < 8:
        return jsonify({'error': 'Password must be at least 8 characters long.'}), 400

    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({'error': 'User already exists.'}), 409
    
    hashed_pw = hash_password(password)

    new_user = User(email=email, password_hash=hashed_pw)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully.'}), 201


def user_login(data):
    email = data.get('email', '').strip()
    password = data.get('password', '').strip()

    if not email or not password:
        return jsonify({'error': 'Email and password are required.'}), 400

    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({'error': 'User does not exist.'}), 404

    if not bcrypt.checkpw(password.encode('utf-8'), user.password_hash):
        return jsonify({'error': 'Invalid credentials, Please try again.'}), 401

    login_user(user)

    return jsonify({'message': 'Login successful.'}), 200


def generate_api_key(user):
    api_key = secrets.token_hex(32)

    hashed_key = APIKey.hash_key(api_key)

    new_api_key = APIKey(key=hashed_key, user_id=user.id)
    db.session.add(new_api_key)
    db.session.commit()

    return jsonify({'api_key': api_key}), 201 


def regenerate_api_key(user):
    old_api_key = APIKey.query.filter_by(user_id=user.id).first()
    if old_api_key:
        db.session.delete(old_api_key)
        db.session.commit()

    return generate_api_key(user)


def validate_api_key(api_key):
    key_record = APIKey.query.filter_by(user_id=current_user.id).first()

    if not key_record:
        return None  # Invalid API key

    # Compare the provided plain-text API key with the stored hashed key
    if bcrypt.checkpw(api_key.encode('utf-8'), key_record.key):
        return key_record.user  # If valid, return the associated user
    return None  # If the API key is invalid


