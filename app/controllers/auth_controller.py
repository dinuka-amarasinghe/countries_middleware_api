from flask import request, redirect, url_for, flash, session, jsonify
from app import db
from app.models import User, APIKey, APIUsage
from app.utils.security import hash_password
from flask_login import login_user, current_user 
import secrets
import bcrypt
import re

def register_user(data):
    email = data.get('email', '').strip()
    password = data.get('password', '').strip()

    # Validation
    if not email or not password:
        return _handle_register_response("Email and password are required.", False)

    if not re.match(r'^\S+@\S+\.\S+$', email):
        return _handle_register_response("Invalid email format.", False)

    if len(password) < 8:
        return _handle_register_response("Password must be at least 8 characters long.", False)

    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return _handle_register_response("User already exists.", False)

    # Create user
    hashed_pw = hash_password(password)
    new_user = User(email=email, password_hash=hashed_pw)
    db.session.add(new_user)
    db.session.commit()

    return _handle_register_response("Registration successful! Please log in.", True)


def _handle_register_response(message, success):
    if request.is_json:
        return jsonify({'message': message}), 201 if success else 400

    flash(message, 'success' if success else 'danger')
    return redirect(url_for('authentication.login' if success else 'authentication.register'))


def user_login(data):
    email = data.get('email', '').strip()
    password = data.get('password', '').strip()

    if not email or not password:
        flash('Email and password are required.', 'danger')
        return redirect(url_for('authentication.login'))

    user = User.query.filter_by(email=email).first()
    if not user:
        flash('User does not exist.', 'danger')
        return redirect(url_for('authentication.login'))

    if not bcrypt.checkpw(password.encode('utf-8'), user.password_hash):
        flash('Invalid credentials, please try again.', 'danger')
        return redirect(url_for('authentication.login'))

    login_user(user)
    flash('Login successful!', 'success')
    return redirect(url_for('authentication.dashboard'))


def generate_api_key(user):
    api_key = secrets.token_hex(32)
    hashed_key = APIKey.hash_key(api_key)

    new_api_key = APIKey(key=hashed_key, user_id=user.id)
    db.session.add(new_api_key)
    db.session.commit()

    session['plain_api_key'] = api_key

    if request.is_json:
        return jsonify({'api_key': api_key}), 201

    flash("API key generated successfully!", "success")
    return redirect(url_for('authentication.dashboard'))


def regenerate_api_key(user):
    old_api_key = APIKey.query.filter_by(user_id=user.id).first()

    if old_api_key:
        APIUsage.query.filter_by(api_key_id=old_api_key.id).delete()
        db.session.delete(old_api_key)
        db.session.commit()

    return generate_api_key(user)


# def validate_api_key(api_key):
#     key_record = APIKey.query.filter_by(user_id=current_user.id).first()

#     if not key_record:
#         return None  

#     if bcrypt.checkpw(api_key.encode('utf-8'), key_record.key):
#         return key_record.user  
#     return None

def validate_api_key(api_key):
    """Check if the given plain-text API key is valid"""
    all_keys = APIKey.query.all()

    for key_record in all_keys:
        stored_key = key_record.key
        if isinstance(stored_key, str):
            stored_key = stored_key.encode('utf-8')

        if bcrypt.checkpw(api_key.encode('utf-8'), stored_key):
            return User.query.get(key_record.user_id)

    return None
