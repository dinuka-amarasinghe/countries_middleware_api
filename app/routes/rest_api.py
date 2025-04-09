from flask import Blueprint
from flask import request, jsonify
from app.controllers.auth_controller import validate_api_key

rest_api_bp = Blueprint('ap', __name__, url_prefix='/api')

@rest_api_bp.route('/countries', methods=['GET'])
def get_countries():
    api_key = request.headers.get('X-API-KEY')
    if not api_key:
        return jsonify({'error': 'API key is required.'}), 400

    user = validate_api_key(api_key)
    if user is None:
        return jsonify({'error': 'Invalid API key.'}), 401

    return jsonify({"message": "Countries data here."}), 200