from flask import Blueprint

base_bp = Blueprint('base', __name__)

@base_bp.route('/')
def index():
    return "Flask App is Running!"
