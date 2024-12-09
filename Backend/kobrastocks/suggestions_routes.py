# suggestions_routes.py

"""
------------------Prologue--------------------
File Name: suggestions_routes.py
Path: Backend/kobrastocks/suggestions_routes.py

Description:
Defines routes for fetching stock suggestions based on user input for the autocomplete feature.

Input:
Query parameter 'query' representing the partial stock ticker or name.

Output:
JSON response containing a list of stock suggestions.

Collaborators: Spencer Sliffe
---------------------------------------------
"""

from flask import Blueprint, request, jsonify, current_app
import requests

suggestions = Blueprint('suggestions', __name__)


@suggestions.route('/api/suggestions', methods=['GET'])
def get_suggestions():
    query = request.args.get('query', '').strip()
    if not query:
        return jsonify({'suggestions': []}), 200

    # Use the Yahoo Finance API to get suggestions
    url = 'https://query2.finance.yahoo.com/v1/finance/search'

    params = {
        'q': query,
        'lang': 'en-US',
        'region': 'US',
        'quotesCount': 5,
        'newsCount': 0,
    }

    headers = {
        'User-Agent': 'Mozilla/5.0',
    }

    try:
        response = requests.get(url, params=params, headers=headers)
        data = response.json()

        suggestions_list = []
        for item in data.get('quotes', []):
            suggestions_list.append({
                'symbol': item.get('symbol'),
                'name': item.get('shortname') or item.get('longname') or item.get('symbol'),
                'exchDisp': item.get('exchDisp'),
            })

        return jsonify({'suggestions': suggestions_list}), 200
    except Exception as e:
        current_app.logger.error(f"Error fetching suggestions: {e}")
        return jsonify({'suggestions': []}), 200

