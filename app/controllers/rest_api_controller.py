from flask import request, jsonify, Response
from flask_login import current_user
from app.controllers.auth_controller import validate_api_key
from app import db
from collections import OrderedDict
import requests
import json
from app.models import APIUsage
import bcrypt

def get_all_countries():
    api_key = request.headers.get('X-API-KEY')
    if not api_key:
        return jsonify({"error": "API key is required."}), 400

    user = validate_api_key(api_key)
    if user != current_user:
        return jsonify({"error": "Invalid API key."}), 401

    try:
        log_api_usage(api_key, '/api/countries')

        response = requests.get('https://restcountries.com/v3.1/all')
        response.raise_for_status()  
        countries = response.json()

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
    api_key = request.headers.get('X-API-KEY')

    print(api_key)

    if not api_key:
        return jsonify({"error": "API key is required."}), 400

    user = validate_api_key(api_key)
    if not user:
        return jsonify({"error": "Invalid API key."}), 401

    try:
        log_api_usage(api_key, f'/api/countries/{country_name}')

        response = requests.get(f'https://restcountries.com/v3.1/name/{country_name}')
        response.raise_for_status() 

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

    
def log_api_usage(api_key_plaintext, endpoint):
    try:
        from app.models import APIKey  

        for key_record in current_user.api_keys:

            stored_hash = key_record.key
            if isinstance(stored_hash, str):
                stored_hash = stored_hash.encode('utf-8')

            if bcrypt.checkpw(api_key_plaintext.encode('utf-8'), stored_hash):
                usage = APIUsage(
                    user_id=current_user.id,
                    api_key_id=key_record.id,
                    endpoint=endpoint
                )
                db.session.add(usage)
                db.session.commit()
                print(f"✅ API usage logged for user {current_user.id} at {endpoint}")
                return

        print("No matching API key found for logging usage")
        return jsonify({"error": "Invalid API key."}), 401

    except Exception as e:
        print(f"Error in log_api_usage: {e}")
        return jsonify({"error": "Error logging API usage."}), 500


