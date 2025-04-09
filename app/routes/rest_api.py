from flask import Blueprint

rest_api_bp = Blueprint('ap', __name__, url_prefix='/api')

@rest_api_bp.route('/api')
def login():
    return "API"