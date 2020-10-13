#!/usr/bin/python3
""" This file sets API """
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
from os import getenv
from flask_cors import CORS

HBNB_API_HOST = getenv('HBNB_API_HOST', "0.0.0.0")
HBNB_API_PORT = int(getenv('HBNB_API_PORT', 5000))

app = Flask(__name__)
app.url_map.strict_slashes = False
app.register_blueprint(app_views)
cors = CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def teardown(self):
    """ This method finish sessions"""
    storage.close()


@app.errorhandler(404)
def page_404(e):
    """ Handler for 404 errors"""
    return jsonify(error="Not found"), 404


if __name__ == "__main__":
    app.run(host=HBNB_API_HOST, port=HBNB_API_PORT, threaded=True)
