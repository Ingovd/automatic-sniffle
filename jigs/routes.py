from flask import (Blueprint,
                   request,
                   current_app as app)

from google.cloud import datastore


jig_bp = Blueprint('jig_bp', __name__)

@jig_bp.route('/', methods=['POST'])
def gather():
    player_id = request.form.get('player_id', '')
    puzzle_id = request.form.get('puzzle_id', '')
    entry_key = app.db.key("log", puzzle_id)
    entry = datastore.Entity(key=entry_key)
    entry[player_id] = player_id
    app.db.put(entry)
    return {player_id: player_id, puzzle_id: puzzle_id}
