from flask import jsonify
from app import db
from app.models import User, APIKey
from app.utils.security import hash_password
from flask_login import login_user, current_user  # Make sure to import login_user
import secrets
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


# def generate_api_key(user):
#     # Generate a secure random API key (using secrets for cryptographic security)
#     api_key = secrets.token_hex(32)  # Generate a 64-character hexadecimal string

#     # Create the API key record
#     new_api_key = APIKey(key=api_key, user_id=user.id)
    
#     # Save to the database
#     db.session.add(new_api_key)
#     db.session.commit()

#     return jsonify({'api_key': api_key}), 201


def generate_api_key(user):
    # Generate a secure random API key
    api_key = secrets.token_hex(32)

    # Hash the generated API key before storing it
    hashed_key = APIKey.hash_key(api_key)

    # Store the hashed key in the database
    new_api_key = APIKey(key=hashed_key, user_id=user.id)
    db.session.add(new_api_key)
    db.session.commit()

    return jsonify({'api_key': api_key}), 201  # Send back the original (unhashed) key for use


def regenerate_api_key(user):
    # First, delete the old API key(s)
    old_api_key = APIKey.query.filter_by(user_id=user.id).first()
    if old_api_key:
        db.session.delete(old_api_key)
        db.session.commit()

    # Then, generate a new API key for the user
    return generate_api_key(user)


def validate_api_key(api_key):
    # Retrieve the API key record from the database
    key_record = APIKey.query.filter_by(user_id=current_user.id).first()

    if not key_record:
        return None  # Invalid API key

    # Compare the provided plain-text API key with the stored hashed key
    if bcrypt.checkpw(api_key.encode('utf-8'), key_record.key):
        return key_record.user  # If valid, return the associated user
    return None  # If the API key is invalid

