from flask import Blueprint, request, jsonify, Response
from flask_login import login_required, current_user
from app.controllers.auth_controller import validate_api_key
import requests
from collections import OrderedDict
import json

rest_api_bp = Blueprint('rest_api', __name__, url_prefix='/api')

# Get all countries (Login Required + API Key Validation)
@rest_api_bp.route('/countries', methods=['GET'])
@login_required
def get_all_countries():
    # Validate API key for the logged-in user
    api_key = request.headers.get('X-API-KEY')
    if not api_key:
        return jsonify({"error": "API key is required."}), 400

    user = validate_api_key(api_key)
    if user != current_user:
        return jsonify({"error": "Invalid API key."}), 401

    try:
        # Request all country data from RestCountries API
        response = requests.get('https://restcountries.com/v3.1/all')
        response.raise_for_status()  # Raise an error for bad status codes
        countries = response.json()

        # Filter the relevant fields for each country
        filtered_countries = []
        for country in countries:
            filtered_country = {
                "name": country.get('name', {}).get('common', ''),
                "currency": country.get('currencies', {}),
                "capital": country.get('capital', [''])[0] if 'capital' in country else '',
                "languages": country.get('languages', {}),
                "flag": country.get('flags', {}).get('png', '')
            }

            # Manually arrange the keys in the desired order
            ordered_country = OrderedDict([
                ('name', filtered_country['name']),
                ('currency', filtered_country['currency']),
                ('capital', filtered_country['capital']),
                ('languages', filtered_country['languages']),
                ('flag', filtered_country['flag'])
            ])

            filtered_countries.append(ordered_country)

        # Convert filtered and ordered data into JSON and return as Response
        json_response = json.dumps(filtered_countries)
        return Response(json_response, mimetype='application/json')

    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Error fetching data: {e}"}), 500


# Get country by name (Login Required + API Key Validation)
@rest_api_bp.route('/countries/<country_name>', methods=['GET'])
@login_required
def get_country_by_name(country_name):
    # Validate API key for the logged-in user
    api_key = request.headers.get('X-API-KEY')
    if not api_key:
        return jsonify({"error": "API key is required."}), 400

    user = validate_api_key(api_key)
    if user != current_user:
        return jsonify({"error": "Invalid API key."}), 401

    try:
        # Request country data from RestCountries API
        response = requests.get(f'https://restcountries.com/v3.1/name/{country_name}')
        response.raise_for_status()  # Check if the request was successful

        country = response.json()

        if not country:
            return jsonify({"error": "Country not found"}), 404

        # Construct the filtered response in the desired order
        country_data = {
            "name": country[0].get('name', {}).get('common', ''),
            "currency": country[0].get('currencies', {}),
            "capital": country[0].get('capital', [''])[0] if 'capital' in country[0] else '',
            "languages": country[0].get('languages', {}),
            "flag": country[0].get('flags', {}).get('png', '')
        }

        # Manually arrange the keys in the desired order
        ordered_response = OrderedDict([
            ('name', country_data['name']),
            ('currency', country_data['currency']),
            ('capital', country_data['capital']),
            ('languages', country_data['languages']),
            ('flag', country_data['flag'])
        ])

        # Convert OrderedDict to JSON manually and return as a Response
        json_response = json.dumps(ordered_response)
        return Response(json_response, mimetype='application/json')

    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Error fetching data: {e}"}), 500
