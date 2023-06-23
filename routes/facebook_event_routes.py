from flask import Blueprint, request, jsonify
import requests
import os
import json

facebook_event_routes = Blueprint('facebook_event_routes', __name__)


@facebook_event_routes.route('/facebook_event', methods=['POST'])
def get_facebook_event():
    event_url = request.json.get('event_url')
    set_facebook_event(event_url)
    response = run_sync_get_dataset_items()

    if response.status_code != 201:
        return jsonify({'error': f"Something went wrong getting {response.text}"}), 500
    else:
        return jsonify(json.loads(response.text)[0]), 200


def set_facebook_event(event_url):
    data = {
        "startUrls": [event_url]
    }
    headers = {'Content-Type': 'application/json'}
    url = get_input_url()

    response = requests.put(url, json=data, headers=headers)

    if response.status_code != 200:
        return jsonify({'error': f"Something went wrong updating the Facebook event {response.text}"}), 500


def run_sync_get_dataset_items():
    url = get_run_sync_url()
    headers = {'Content-Type': 'application/json'}

    response = requests.post(url, headers=headers)
    return response


def get_input_url():
    TOKEN = os.environ.get(
        'APIFY_TOKEN') or "apify_api_yyMUFgQ7LP1MSE0N0WFVcmgUSBdLzH44Nbuw"
    TASK = os.environ.get(
        'APIFY_TASK') or "notable_sitar~facebook-events-scraper-task"
    return f"https://api.apify.com/v2/actor-tasks/{TASK}/input?token={TOKEN}"


def get_run_sync_url():
    TOKEN = os.environ.get(
        'APIFY_TOKEN') or "apify_api_yyMUFgQ7LP1MSE0N0WFVcmgUSBdLzH44Nbuw"
    TASK = os.environ.get(
        'APIFY_TASK') or "notable_sitar~facebook-events-scraper-task"
    return f"https://api.apify.com/v2/actor-tasks/{TASK}/run-sync-get-dataset-items?token={TOKEN}"
