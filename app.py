from flask import Flask
from routes.facebook_event_routes import facebook_event_routes
from routes.fuzzy_match_routes import fuzzy_match_routes
from routes.events_on_day_routes import events_on_day_routes
from routes.youtube_routes import youtube_routes
app = Flask(__name__)

app.register_blueprint(facebook_event_routes)
app.register_blueprint(fuzzy_match_routes)
app.register_blueprint(events_on_day_routes)
app.register_blueprint(youtube_routes)

if __name__ == '__main__':
    app.run()
