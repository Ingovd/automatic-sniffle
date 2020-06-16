import json

from flask import (Blueprint,
                   request,
                   abort,
                   current_app as app)

from google.cloud import datastore


jig_bp = Blueprint('jig_bp', __name__)

@jig_bp.route('/', methods=['POST'])
def gather():
    if not (data := request.get_json(silent=True)):
        abort(415)
    if not (playerSecret := data.get("playerSecret")):
        abort(400)
    if not (puzzleID := data.get("puzzleID")):
        abort(400)
    if not (events := data.get("events")):
        abort(400)
    if not isinstance(events, dict):
        abort(400)
    player_key = app.db.key("player", playerSecret)
    player = datastore.Entity(key=player_key)
    puzzle_key = app.db.key("puzzle", puzzleID, parent=player_key)
    entry = datastore.Entity(key=puzzle_key)
    for key, value in events.items():
        entry[key] = json.dumps(value)
    app.db.put(player)
    app.db.put(entry)
    return app.response_class(status=200)
