from flask import Blueprint, request, jsonify
import sys
import requests
import os
import datetime
script_dir = os.path.dirname(os.path.abspath(__file__))
mongo_python_dir = os.path.join(script_dir, '..', 'mongo-python')
sys.path.append(mongo_python_dir)
import upload_to_mongo

events_on_day_routes = Blueprint('events_on_day_routes', __name__)
API_TOKEN = "AIzaSyBNlYH01_9Hc5S1J9vuFmu2nUqBZJNAXxs&"

@events_on_day_routes.route('/events_on_day', methods=['POST'])
def get_events_on_day():
    date = request.json.get('date')
    events = fetch_events_on_day(date)

    if not events:
        return jsonify({'error': 'No events found for the given date'}), 404

    formatted_events = format_events(events)
    return jsonify({'events': formatted_events}), 200


def fetch_events_on_day(date):
    date_splited = date.split("-")
    new_date = datetime.datetime(int(date_splited[0]), int(
        date_splited[1]), int(date_splited[2])) + datetime.timedelta(days=1)
    year = new_date.strftime("%Y")
    month = new_date.strftime("%m")
    day = new_date.strftime("%d")
    next_day = f"{year}-{month}-{day}"
    url = (f"https://clients6.google.com/calendar/v3/"
           f"calendars/info@aptaliko.gr/events?calendarId=info%40aptaliko.gr"
           f"&singleEvents=true&timeZone=Europe%2FAthens&maxAttendees=1&"
           f"maxResults=100&sanitizeHtml=true&timeMin={date}T00%3A00%3A00%2B03%3A00&"
           f"timeMax={next_day}T00%3A00%3A00%2B03%3A00&key={API_TOKEN}")

    response = requests.get(url)
    results = response.json()

    if 'items' in results:
        return results['items']
    else:
        return []


def format_events(events):
    bands = list(upload_to_mongo.get_all_bands())
    bands = list(map(lambda dic: dic['name'], bands))
    items = []
    dic_of_summaries = {}
    new_events = []

    for event in events:
        if 'summary' in event:
            if event['summary'] not in dic_of_summaries:
                new_events.append(event)
                dic_of_summaries[event['summary']] = 1

    events = new_events

    for event in events:
        time = event['start']['dateTime'].split("T")[1][0:5]
        endTime = (int(time[0:2]) + 4) % 24
        endTime = str(endTime)+":00" if endTime >= 10 else "0" + \
            str(endTime)+":00"
        start = event['start']['dateTime'].split("T")[0].split("-")
        date = f"{start[2]}-{start[1]}-{start[0]}"
        description = ''
        if 'description' in event:
            description = event['description']
        summary = ''
        if 'summary' in event:
            summary = event['summary']
        location = event['location'].split(',')[0]
        band = compare_a_string_with_a_list_of_strings(summary, bands)

        dic = {
            "location": location,
            "summary": summary,
            "band": band,
            "date": date,
            "startTime": time,
            "description": description,
            "endTime": endTime,
        }
        items.append(dic)

    return items


def compare_a_string_with_a_list_of_strings(s: str, l: list):
    maxy = 0
    string = ''

    for ss in l:
        s1 = ss.split()
        s1 = list(filter(lambda word: word != "-", s1))
        temp = evaluate_string_with_string(s1, s)

        if temp > maxy:
            maxy = temp
            string = ss

    return string


def evaluate_string_with_string(s1: str, s2: str):
    total = 0

    for word in s1:
        w, maxy = which_word_from_string(s2, word)
        total += maxy

    return total


def which_word_from_string(s: str, w: str):
    splited = s.split()
    maxy = 0
    word = ''

    for sp in splited:
        if sp != "-":
            wr_sm = words_similarity(sp, w)

            if wr_sm > maxy:
                word = sp
                maxy = wr_sm

    return (word, maxy)


def words_similarity(w1: str, w2: str):
    if len(w1) < len(w2):
        temp = w1
        w1 = w2
        w2 = temp
    count = 0

    for s in w2:
        if s != w1[count]:
            break
        count += 1

    return count/len(w1)
