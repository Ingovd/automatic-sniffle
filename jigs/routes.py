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
    player_key = app.db.key("player", data["playerSecret"])
    player = datastore.Entity(key=player_key)
    puzzle_key = app.db.key("puzzle", data["puzzleID"], parent=player_key)
    entry = datastore.Entity(key=puzzle_key)
    for key, value in data["events"].items():
        entry[key] = json.dumps(value)
    app.db.put(player)
    app.db.put(entry)
    return data
