from flask import Blueprint, request
from flask_login import login_required
from app.controllers.rest_api_controller import get_all_countries, get_country_by_name

rest_api_bp = Blueprint('rest_api', __name__, url_prefix='/api')

@rest_api_bp.route('/countries', methods=['GET'])
@login_required
def all_countries():
    return get_all_countries()


@rest_api_bp.route('/countries/<country_name>', methods=['GET'])
@login_required
def country_by_name(country_name):
    return get_country_by_name(country_name)


   


