from pathlib import Path

from flask import Flask, request, send_file

from background_remover import default_init, img_from_url

app = Flask(__name__)
remover = default_init()


@app.route('/', methods=["POST"])
def remove_background():
    filename = "tmp.jpg"
    Path(filename).unlink(missing_ok=True)
    url = request.json["url"]
    remover.remove_background(img_from_url(url), filename)
    return send_file(filename, mimetype='image/jpeg')

# export FLASK_APP=api
# flask run
