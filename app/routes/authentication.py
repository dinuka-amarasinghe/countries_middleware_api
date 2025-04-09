from flask import Blueprint, request, jsonify
from flask_login import login_required, logout_user, current_user
from app.controllers.auth_controller import register_user, user_login, generate_api_key, regenerate_api_key

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
    logout_user()  
    return jsonify({'message': 'Logged out successfully.'}), 200


@authentication_blueprint.route('/generate-api-key', methods=['POST'])
@login_required
def generate_key():
    return generate_api_key(current_user)


@authentication_blueprint.route('/regenerate-api-key', methods=['POST'])
@login_required
def regenerate_key():
    return regenerate_api_key(current_user)

