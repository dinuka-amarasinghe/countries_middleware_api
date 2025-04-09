from flask import jsonify
from app import db
from app.models import User
from app.utils.security import hash_password
from flask_login import login_user  # Make sure to import login_user
import bcrypt
import re

def register_user(data):
    email = data.get('email', '').strip()
    password = data.get('password', '').strip()

    # Input presence check
    if not email or not password:
        return jsonify({'error': 'Both email and password are required.'}), 400

    # Email format validation
    email_regex = r'^\S+@\S+\.\S+$'
    if not re.match(email_regex, email):
        return jsonify({'error': 'Invalid email format.'}), 400

    # Password strength check
    if len(password) < 8:
        return jsonify({'error': 'Password must be at least 8 characters long.'}), 400

    # Check if user already exists
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({'error': 'User already exists.'}), 409

    # Hash password
    hashed_pw = hash_password(password)

    # Create user
    new_user = User(email=email, password_hash=hashed_pw)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully.'}), 201


def user_login(data):
    email = data.get('email', '').strip()
    password = data.get('password', '').strip()

    # Input presence check
    if not email or not password:
        return jsonify({'error': 'Email and password are required.'}), 400

    # Check if user exists
    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({'error': 'User does not exist.'}), 404

    # Check if password matches
    if not bcrypt.checkpw(password.encode('utf-8'), user.password_hash):
        return jsonify({'error': 'Invalid credentials, Please try again.'}), 401

    # Log in the user with Flask-Login
    login_user(user)

    return jsonify({'message': 'Login successful.'}), 200
