from flask import request, jsonify, Response
from flask_login import login_required, current_user
from app.controllers.auth_controller import validate_api_key
from app import db
from collections import OrderedDict
import requests
import json
from app.models import APIUsage


def get_all_countries():
    # Validate API key for the logged-in user
    api_key = request.headers.get('X-API-KEY')
    if not api_key:
        return jsonify({"error": "API key is required."}), 400

    user = validate_api_key(api_key)
    if user != current_user:
        return jsonify({"error": "Invalid API key."}), 401

    try:
        # Log API key usage
        log_api_usage(api_key, '/api/countries')

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
            filtered_countries.append(filtered_country)

        # Manually arrange the keys in the desired order for the entire list of countries
        ordered_countries = [
            OrderedDict([
                ('name', country['name']),
                ('currency', country['currency']),
                ('capital', country['capital']),
                ('languages', country['languages']),
                ('flag', country['flag'])
            ])
            for country in filtered_countries
        ]

        json_response = json.dumps(ordered_countries)
        return Response(json_response, mimetype='application/json')

    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Error fetching data: {e}"}), 500

    

def get_country_by_name(country_name):
    # Validate API key for the logged-in user
    api_key = request.headers.get('X-API-KEY')
    if not api_key:
        return jsonify({"error": "API key is required."}), 400

    user = validate_api_key(api_key)
    if user != current_user:
        return jsonify({"error": "Invalid API key."}), 401

    try:
        # Log API key usage
        log_api_usage(api_key, f'/api/countries/{country_name}')

        # Request country data from RestCountries API
        response = requests.get(f'https://restcountries.com/v3.1/name/{country_name}')
        response.raise_for_status()  # Check if the request was successful

        country = response.json()

        if not country:
            return jsonify({"error": "Country not found"}), 404

        country_data = {
            "name": country[0].get('name', {}).get('common', ''),
            "currency": country[0].get('currencies', {}),
            "capital": country[0].get('capital', [''])[0] if 'capital' in country[0] else '',
            "languages": country[0].get('languages', {}),
            "flag": country[0].get('flags', {}).get('png', '')
        }

        ordered_response = OrderedDict([
            ('name', country_data['name']),
            ('currency', country_data['currency']),
            ('capital', country_data['capital']),
            ('languages', country_data['languages']),
            ('flag', country_data['flag'])
        ])

        json_response = json.dumps(ordered_response)
        return Response(json_response, mimetype='application/json')

    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Error fetching data: {e}"}), 500

    

def log_api_usage(api_key, endpoint):
    """ Log API key usage to the database by storing the accessed endpoint """
    try:
        # Log the API usage with the provided API key and endpoint
        usage = APIUsage(api_key=api_key, endpoint=endpoint)
        db.session.add(usage)
        db.session.commit()  # Commit to the database
        print(f"API usage logged for api_key {api_key} for endpoint {endpoint}")
    except Exception as e:
        print(f"Error in log_api_usage: {e}")
