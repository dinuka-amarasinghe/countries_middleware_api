from flask import Blueprint, request, jsonify
from flask_login import login_required
from app.controllers.auth_controller import register_user
from app.controllers.auth_controller import user_login
from flask_login import logout_user

authentication_blueprint = Blueprint('authentication', __name__, url_prefix='/auth')

@authentication_blueprint.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    return register_user(data)

@authentication_blueprint.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    return user_login(data)

# Non-protected dashboard route
@authentication_blueprint.route('/dashboard', methods=['GET'])
@login_required
def dashboard():
    return "This Is Your Dashboard!"

@authentication_blueprint.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()  # This will log out the user and clear the session
    return jsonify({'message': 'Logged out successfully.'}), 200