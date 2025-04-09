from flask import Blueprint

api_bp = Blueprint('ap', __name__, url_prefix='/api')

@api_bp.route('/api')
def login():
    return "API"