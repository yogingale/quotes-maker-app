from app.tables import tables_bp
from flask_login import login_required
from flask import current_app, render_template, url_for, jsonify
from app.services.spotify_services import get_top_30
from random import randint
import time


@tables_bp.route("/", methods=["GET"])
@login_required
def tables():
    top_30_songs_url = (
        current_app.config["spotify_top_30_url"]
        if "spotify_top_30_url" in current_app.config
        else "https://open.spotify.com/user/thesoundsofspotify/playlist/1z1LfuAoQQDRKLOyVQvaRa"
    )
    top_30_songs = get_top_30(top_30_songs_url)
    print(top_30_songs)
    return render_template(
        "tables/tables.html", table_title="Spotify Top 30 Jam", data=top_30_songs
    )


@tables_bp.route("/dyndata", methods=["GET"])
@login_required
def dyn_data():
    print("dyn data called")
    time.sleep(randint(1, 3))

    columns = []
    for i in range(1, randint(3, 6) + 1):
        columns.append(f"Column {i}")

    rows = []
    for i in range(0, randint(10, 30)):
        row = {}
        for x in columns:
            row[x] = randint(0, 20)
        rows.append(row)

    data = {"rows": rows, "columns": columns}
    return jsonify(data)
