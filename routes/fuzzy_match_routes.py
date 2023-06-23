from flask import Blueprint, request, jsonify
from fuzzywuzzy import fuzz

fuzzy_match_routes = Blueprint('fuzzy_match_routes', __name__)


@fuzzy_match_routes.route('/fuzzy_match', methods=['POST'])
def fuzzy_match():
    bands = request.json.get('bands')
    description = request.json.get('description')

    if not bands or not description:
        return jsonify({'error': 'Invalid request parameters'}), 400

    best_match = get_best_band_match(bands, description)

    return jsonify({'best_match': best_match}), 200


def get_best_band_match(bands, description):
    best_match = ''
    highest_score = 0

    for band in bands:
        score = fuzz.ratio(band.lower(), description.lower())
        if score > highest_score:
            highest_score = score
            best_match = band

    return best_match
